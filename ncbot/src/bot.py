import asyncio
import collections
import json
import logging
import operator
from datetime import datetime

from user import add_users
from user.users import Users

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from common.config import TELEGRAM_API_TOKEN

import matplotlib

import paramiko

import psutil

from server.servers import Servers

from url import add_url
from url.check_ssl import check_ssl_cirt
from url.urls import Urls


logging.basicConfig(filename="bot.log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

matplotlib.use("Agg")

adminid_list = []
path_to_js = './db/db_keys.json'

with open(path_to_js) as _f:
    data = json.load(_f)
    telegrambot = data['telegrambot']
    for i in data['structure']:
        host_s = i['host']
        username_s = i['username']
        pr_key = i['private_key']
    for i in data['adminchatid']:
        adminid_list.append(i)
_f.close()

API_TOKEN = TELEGRAM_API_TOKEN
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

memorythreshold = 70  # If memory usage more this %
poll = 120  # 120 секунд, каждые 2 минуты

shellexecution = []
time_list = []
mem_list = []
xaxis = []
setting_memth = []
set_polling = []
graph_start = datetime.now()


# States
class Form(StatesGroup):
    url = State()
    set_poll = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
        Отправляет приветственное сообщение и помощь по боту.
        Добавляет пользователя в базу данных /password
    """
    await message.answer("Бот для работы с серверами:\n\n"
                         "   /[password for subscribe] - подписаться на сообщения \n"
                         "   /unsubscribe - отписаться от сообщений\n"
                         "   ______________________________________________________ \n"
                         "Работа с серверами: \n"
                         "   /servers - список серверов \n"
                         "   ______________________________________________________ \n"
                         "Работа с url: \n"
                         "   /urls - список url \n"
                         "   /add_url - добавление url в список\n"
                         "   /check_all_ssl - проверка ssl сертификата\n"
                         "   ______________________________________________________ \n"
                         "Работа с пользователями: \n"
                         "   /users - список пользователей \n"
                         "   ______________________________________________________ \n"
                         "Помощь, доп. команды: \n"
                         "   /help - список команд \n"
                         "   /help_leopay - команды Leopay (В разработке)\n"
                         "   /alarm_status - статус флагов тревоги\n"
                         "   /stats - cтаты сервера бота \n"
                         "   /set_poll - период рассылки в секундах(больше 10 секунд)(В разработке)\n"
                         "Рассылка списка серверов с малым количеством памяти\n"
                         "   ______________________________________________________ \n"
                         "\n")


@dp.message_handler(commands=['servers'])
async def servers_list(message: types.Message):
    """Отправляет список серверов"""
    servers = Servers()
    servers = servers.get_all_servers()
    answer_message = "Список серверов:\n    " + \
                     ("\n    ".join([s['username'] + '@' + "".join(s['host']) for s in servers]))
    await message.answer(answer_message)


@dp.message_handler(commands=['users'])
async def users_list(message: types.Message):
    """Отправляет список пользователей"""
    users = Users()
    users = users.get_all_users()
    answer_message = "Список пользователей:\n    " + \
                     ("\n    ".join(['id: ' + u['chat_id'] for u in users]))
    await message.answer(answer_message)


@dp.message_handler(commands=['urls'])
async def urls_list(message: types.Message):
    """ Отправляет список url """
    urls = Urls()
    urls = urls.get_all_urls()
    answer_message = "Список url:\n    " + \
                     ("\n    ".join(['url: ' + u['url'] for u in urls]))
    await message.answer(answer_message, disable_web_page_preview=True)


@dp.message_handler(commands=['check_all_ssl'])
async def check_all_ssl(message: types.Message):
    """ Проверяет url на ssl сертификат """
    urls = Urls()
    urls = urls.get_all_urls()
    data_3 = check_ssl_cirt(urls)

    new_urls = []
    for u in urls:
        new_urls.append(u['url'])
    valid_list = list(map(list, zip(new_urls, data_3)))

    new_valid_list = []
    for j in valid_list:
        new_valid_list.append(j[0] + ', ssl: ' + j[1])

    answer_message = "Список url:\n    " + \
                     ("\n    ".join(['url: ' + u for u in new_valid_list]))
    await message.answer(answer_message, disable_web_page_preview=True)


@dp.message_handler(commands=['unsubscribe'])
async def del_user(message: types.Message):
    """ Удаляет пользователя из базы данных """
    add_users.delete_user(message.from_user.id)
    answer_message = "Вы отписались от сообщений"
    await message.answer(answer_message)


@dp.message_handler(commands=['stats'])
async def server_stats(message: types.Message):
    """ Отправляет статы сервера """
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    time_dif = "Online for: %.1f Hours" % (((now - boot_time).total_seconds()) / 3600)
    mem_total = "Total memory: %.2f GB " % (memory.total / 1000000000)
    mem_avail = "Available memory: %.2f GB" % (memory.available / 1000000000)
    mem_use_perc = "Used memory: " + str(memory.percent) + " %"
    disk_used = "Disk used: " + str(disk.percent) + " %"
    pids = psutil.pids()
    pids_reply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            p_mem = p.memory_percent()
            if p_mem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += p_mem
                else:
                    procs[p.name()] = p_mem
        except RuntimeError:
            logging.exception("RuntimeError at def stats")
    sorted_procs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sorted_procs:
        pids_reply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"

    reply = "\n".join([
        time_dif,
        mem_total,
        mem_avail,
        mem_use_perc,
        disk_used,
    ])
    reply += "\n\n{}".format(pids_reply)
    await message.answer(reply)


@dp.message_handler(commands='add_url')
async def add_url_def(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.url.set()

    await message.reply("Введите url без 'http', 'https', '/'...\n"
                        "/cancel - отмена")


@dp.message_handler(commands='set_poll')
async def set_poll_def(message: types.Message):
    """ Set polling function """
    await Form.set_poll.set()

    await message.reply("Введите время в секундах...\n"
                        "/cancel - отмена")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Отмена формы
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.url)
async def process_url(message: types.Message, state: FSMContext):
    """
    Process adding url
    """
    async with state.proxy() as ur_link:
        ur_link['url'] = message.text
    add_url.add_url(ur_link['url'])
    await state.finish()
    await message.answer("Ваш url добавлен в базу данных")


@dp.message_handler(state=Form.set_poll)
async def process_set_poll(message: types.Message, state: FSMContext):
    """
    Process set polling
    """
    global poll
    async with state.proxy() as st_poll:
        st_poll['poll'] = message.text
    poll = st_poll['poll']
    await state.finish()
    await message.answer("Polling:{} секунд".format(poll))


@dp.message_handler(commands=['alarm_status'])
async def alarm_status(message: types.Message):
    alarm_list = []
    name_list = []
    host_list = []
    process_list = []
    alarm_list2 = []
    structure_num = 0
    with open(path_to_js) as _f2:
        data_a_2 = json.load(_f2)
        for host in data_a_2['structure']:
            host_list.append(host['host'])
            structure_num += 1
        for alarm in data_a_2['structure']:
            if alarm['alarm_status'] == [0]:
                alarm_list.append('OK')
            else:
                alarm_list.append('ALARM')
        for name in data_a_2['structure']:
            name_list.append(name['username'])
        for value in data_a_2['Leopay']['alarm_status']['function_leopay']:
            process_list.append(value)
            for value_2 in data_a_2['Leopay']['alarm_status']['function_leopay']['{}'.format(value)]:
                alarm_list2.append(value_2)
    reply = ""
    for struc in range(structure_num):
        reply += "{}@".format(name_list[struc]) + "{}: ".format(host_list[struc]) + \
                 "{}\n".format(alarm_list[struc])
    for struc in range(len(data_a_2['Leopay']['alarm_status']['function_leopay'])):
        reply += "Leopay: {}:".format(process_list[struc]) + "{}\n".format(alarm_list2[struc])
    await message.answer(reply)


@dp.message_handler(commands=['password'])
async def add_user(message: types.Message):
    """Добавляет нового пользователя"""
    add_users.add_user(str(message.from_user.id))
    answer_message = (
        "Вы подписались на сообщения.")
    await message.answer(answer_message)


async def periodic(sleep_for):
    global mem_list
    xx = 0
    while True:
        await asyncio.sleep(sleep_for)
        for d in data['structure']:
            host_temp = d['host']
            username_temp = d['username']
            pr_key_temp = d['private_key']

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            path_key = pr_key_temp
            privkey = paramiko.RSAKey.from_private_key_file(path_key)
            try:
                ssh.connect(hostname=host_temp, username=username_temp, pkey=privkey)
                logging.debug("Connect Server")
            finally:
                logging.debug("Finally Connect Server")
                ssh.close()
            disk = psutil.disk_usage('/')
            disk_free = disk.free

            mem_ck = psutil.virtual_memory()
            mem_percent = mem_ck.percent
            if len(mem_list) > 300:
                mem_q = collections.deque(mem_list)
                mem_q.append(mem_percent)
                mem_q.popleft()
                mem_list = mem_q
                mem_list = list(mem_list)
            else:
                xaxis.append(xx)
                xx += 1
                mem_list.append(mem_percent)
            if mem_percent > memorythreshold:
                memavail = "Available memory: %.2f GB" % (mem_ck.available / 1000000000)
                reply = "{}@{}\nCRITICAL! LOW MEMORY!\n{}\n{}".format(username_temp, host_temp, memavail, disk_free)
                for chat_id in adminid_list:
                    await bot.send_message(chat_id, reply, disable_notification=True)
                # Устанавливаем флаг тревоги
                with open(path_to_js) as f:
                    data_a = json.load(f)
                    if 0 in data_a['structure'][0]['alarm_status']:
                        data_a['structure'][0]['alarm_status'].remove(0)
                        data_a['structure'][0]['alarm_status'].append(1)
                with open(path_to_js, 'w') as f:
                    json.dump(data_a, f, ensure_ascii=False, indent=4)
                _f.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(poll))
    executor.start_polling(dp)
