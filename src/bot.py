import asyncio
import logging
import operator
import os
from datetime import datetime

from user import add_users
from user.users import ChatUsers

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from common import db

import paramiko

import psutil

from server.servers import Keys, Servers

from url import add_url
from url.check_ssl import check_ssl_cirt
from url.urls import Urls


logging.basicConfig(filename="bot.log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

memorythreshold_pc = 5  # Если больше 95% занято (5% свободно)
memorythreshold_gb = 2  # Если меньше 2Gb свободно
poll = 900               # каждые 15 минут(900секунд)


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
                         "   /subscribe - подписаться на сообщения \n"
                         "   /unsubscribe - отписаться от сообщений\n"
                         "   /forget_me - удаляет вас из базы данных\n"
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
                         "   /alarm_status - статус флагов тревоги\n"
                         "   /stats - cтаты сервера бота \n"
                         "Рассылка списка серверов с малым количеством памяти\n"
                         "   ______________________________________________________ \n"
                         "\n")


@dp.message_handler(commands=['servers'])
async def servers_list(message: types.Message):
    """Отправляет список серверов"""
    servers = Servers()
    servers = servers.get_all_servers()
    answer_message = "Список серверов:\n    " + \
                     ("\n    ".join(servers))
    await message.answer(answer_message)


@dp.message_handler(commands=['users'])
async def users_list(message: types.Message):
    """Отправляет список пользователей"""
    users = ChatUsers()
    users = users.get_all_chat_users()
    answer_message = "Список пользователей:\n    " + \
                     ("\n    ".join(['id: ' + str(u) for u in users]))
    await message.answer(answer_message)


@dp.message_handler(commands=['urls'])
async def urls_list(message: types.Message):
    """ Отправляет список url """
    urls = Urls()
    urls = urls.get_all_urls()
    answer_message = "Список url:\n    " + \
                     ("\n    ".join(['url: ' + str(u) for u in urls]))
    await message.answer(answer_message, disable_web_page_preview=True)


@dp.message_handler(commands=['check_all_ssl'])
async def check_all_ssl(message: types.Message):
    """ Проверяет url на ssl сертификат """
    urls = Urls()
    urls = urls.get_all_urls()
    new_urls = []
    for u in urls:
        u = u.replace('http://', '')
        u = u.replace('https://', '')
        u = u.replace('/', '')
        new_urls.append(u)
    data_3 = check_ssl_cirt(new_urls)

    new_urls = []
    for u in urls:
        new_urls.append(u)
    valid_list = list(map(list, zip(new_urls, data_3)))

    new_valid_list = []
    for j in valid_list:
        new_valid_list.append(j[0] + ', ssl: ' + j[1])

    answer_message = "Список url:\n    " + \
                     ("\n    ".join(['url: ' + u for u in new_valid_list]))
    await message.answer(answer_message, disable_web_page_preview=True)


@dp.message_handler(commands=['unsubscribe'])
async def unsub(message: types.Message):
    """ Удаляет пользователя из базы данных """
    add_users.unsubscribe(message.from_user.id)
    answer_message = "Вы отписались от сообщений"
    await message.answer(answer_message)


@dp.message_handler(commands=['forget_me'])
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

    servers = Servers()
    servers = servers.get_all_servers_with_alarm()
    answer_message = "Список серверов с тревогой:\n    " + \
                     ("\n    ".join(servers))
    await message.answer(answer_message)


@dp.message_handler(commands=['subscribe'])
async def add_user(message: types.Message):
    """Добавляет нового пользователя"""
    add_users.add_user(str(message.from_user.id))
    answer_message = (
        "Вы подписались на сообщения.")
    await message.answer(answer_message)


async def periodic(sleep_for):
    while True:
        await asyncio.sleep(sleep_for)
        servers = Servers()
        servers = servers.get_all_servers()
        hosts = []
        usernames = []
        for r in servers:
            n = (r.split('@'))
            host = n[1]
            usname = n[0]

            hosts.append(host)
            usernames.append(usname)
        keys = Keys()
        keys = keys.get_all_keys()

        for i in range(len(hosts)):
            host_temp = hosts[i]
            username_temp = usernames[i]
            pr_key_temp = "src/db/" + keys[i]
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            path_key = pr_key_temp
            privkey = paramiko.RSAKey.from_private_key_file(path_key)
            try:
                ssh.connect(hostname=host_temp, username=username_temp, pkey=privkey)
                logging.debug("Connect Server")
            finally:
                logging.debug("Finally Connect Server")
                stdin, stdout, stderr = ssh.exec_command('df --output=pcent /home')
                pcent = []
                for line in stdout:
                    pcent.append(line.strip('\n'))

                stdin, stdout, stderr = ssh.exec_command('df --output=avail --block-size=G /home')
                mem_avail_gb = []
                for line in stdout:
                    mem_avail_gb.append(line.strip('\n'))

                ssh.close()
            pcent_num = pcent[1].replace('%', '')
            pcent_num = int(pcent_num.replace(' ', ''))
            mem_avail_gb_num = mem_avail_gb[1].replace('G', '')
            mem_avail_gb_num = int(mem_avail_gb_num.replace(' ', ''))
            if ((100 - pcent_num) <= memorythreshold_pc) or (mem_avail_gb_num <= memorythreshold_gb):
                db.set_alarm_server(host_temp)
                reply = """{}@{}\nCRITICAL! LOW MEMORY!\n{}%\n{}Gb""".format(
                    username_temp,
                    host_temp,
                    pcent_num,
                    mem_avail_gb_num)
                users = ChatUsers()
                users = users.get_all_chat_users_with_sub()
                for chat_id in users:
                    await bot.send_message(chat_id, reply, disable_notification=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(poll))
    executor.start_polling(dp)
