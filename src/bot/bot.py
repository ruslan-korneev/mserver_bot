import asyncio
import logging
import operator
import os
from datetime import datetime
from io import StringIO
from multiprocessing.dummy import Pool as ThreadPool

from user import add_users
from user.users import ChatUsers

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from common import db

import paramiko
from paramiko.ssh_exception import SSHException

import psutil

from server.servers import Keys, Servers

from url import add_url
from url import getcode200
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
                         "   /all_users - список всех пользователей \n"
                         "   /users_with_subscribe - список пользователей с подпиской \n"
                         "   ______________________________________________________ \n"
                         "Помощь, доп. команды: \n"
                         "   /help - список команд \n"
                         "   /alarm_status - статус флагов тревоги\n"
                         "   /fix url server - если починил что-либо\n"
                         "         (url или названия сервера через пробел)\n"
                         "         (сервер писать в формате username@host)\n"
                         "         (url писать также, как и при его добавлении)\n"
                         "   /stats - cтаты сервера бота \n"
                         "Рассылка:\n"
                         "      списка серверов с малым количеством памяти.\n"
                         "      списка url с истекшим SSL, или ошибкой при открытии\n"
                         "   ______________________________________________________ \n"
                         "\n")


@dp.message_handler(commands=['servers'])
async def servers_list(message: types.Message):
    """Отправляет список серверов"""
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем список серверов...')
        await asyncio.sleep(1)
        servers = Servers()
        servers = servers.get_all_servers()
        answer_message = "Список серверов:\n    " + \
                         ("\n    ".join(servers))
        await message.answer(answer_message)
    else:
        await message.reply('У вас не достаточно прав')


@dp.message_handler(commands=['all_users'])
async def users_list(message: types.Message):
    """Отправляет список пользователей"""
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем список пользователей...')
        await asyncio.sleep(1)
        users = ChatUsers()
        names, surnames, usernames = users.get_all_chat_users()
        users = []
        for i in range(len(names)):
            users.append('{} {}, @{}'.format(names[i], surnames[i], usernames[i]))
        answer_message = "Список пользователей:\n    " + \
                         ("\n    ".join(['' + str(u) for u in users]))
        await message.answer(answer_message)
    else:
        await message.reply('У вас не достаточно прав')


@dp.message_handler(commands=['users_with_subscribe'])
async def users_list_with_subscribe(message: types.Message):
    """Отправляет список пользователей"""
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем список пользователей...')
        await asyncio.sleep(1)
        users = ChatUsers()
        names, surnames, usernames, chat_ids = users.get_all_chat_users_with_sub()
        users = []
        for i in range(len(names)):
            users.append('{} {}, @{}'.format(names[i], surnames[i], usernames[i]))
        answer_message = "Список пользователей:\n    " + \
                         ("\n    ".join(['' + str(u) for u in users]))
        await message.reply(answer_message)
    else:
        await message.reply('У вас не достаточно прав')


@dp.message_handler(commands=['urls'])
async def urls_list(message: types.Message):
    """ Отправляет список url """
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем список url...')
        await asyncio.sleep(1)
        urls = Urls()
        urls = urls.get_all_urls()
        answer_message = "Список url:\n    " + \
                         ("\n    ".join(['url: ' + str(u) for u in urls]))
        await message.answer(answer_message, disable_web_page_preview=True)
    else:
        await message.reply('У вас не достаточно прав.')


@dp.message_handler(commands=['check_all_ssl'])
async def check_all_ssl(message: types.Message):
    """ Проверяет url на ssl сертификат """
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем список url...')
        await asyncio.sleep(1)

        urls = Urls()
        urls = urls.get_all_urls()

        await message.reply('Проверяем ssl-сертификаты...')
        await asyncio.sleep(1)

        data_3 = check_ssl_cirt(urls)
        valid_list = list(map(list, zip(urls, data_3)))

        await asyncio.sleep(1)

        new_valid_list = []
        for j in valid_list:
            if 'invalid' in j[1]:
                db.set_alarm_url(j[0])
            new_valid_list.append(j[0] + ', ssl: ' + j[1])

        answer_message = "Список url:\n    " + \
            ("\n    ".join(['url: ' + u for u in new_valid_list]))
        await message.answer(answer_message, disable_web_page_preview=True)
    else:
        await message.reply('У вас не достаточно прав.')


@dp.message_handler(commands=['unsubscribe'])
async def unsub(message: types.Message):
    """ Удаляет пользователя из базы данных """
    await message.reply('Секундочку..')

    await asyncio.sleep(1)
    add_users.unsubscribe(str(message.from_user.id))
    answer_message = "Вы отписались от сообщений"
    await message.answer(answer_message)


@dp.message_handler(commands=['forget_me'])
async def del_user(message: types.Message):
    """ Удаляет пользователя из базы данных """
    await message.reply('Удаляем вас из базы данных...')
    await asyncio.sleep(1)

    add_users.delete_user(message.from_user.id)
    answer_message = "Вы отписались от сообщений"
    await message.reply(answer_message)


@dp.message_handler(commands=['stats'])
async def server_stats(message: types.Message):
    """ Отправляет статы сервера """
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        await message.reply('Собираем информацию...')
        await asyncio.sleep(1)

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
        await message.reply(reply)
    else:
        await message.reply('У вас не достаточно прав.')


@dp.message_handler(commands='add_url')
async def add_url_def(message: types.Message):
    """
    Conversation's entry point
    """
    if db.access_check_admin(str(message.from_user.id)):
        # Set state
        await Form.url.set()

        await message.reply("Введите url ...\n"
                            "/cancel - отмена")
    else:
        await message.reply('У вас не достаточно прав.')


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
    await message.reply('Отменяем ...')
    await asyncio.sleep(1)
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
    await message.reply('Добавляем в базу данных ...')
    await asyncio.sleep(1)
    await message.reply("Ваш url добавлен в базу данных")


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
    if (db.access_check_collegue(str(message.from_user.id)) or db.access_check_admin(str(message.from_user.id))):
        servers = Servers()
        servers = servers.get_all_servers_with_alarm()
        if servers:
            answer_message = "Список серверов с тревогой:\n    " + \
                             ("\n    ".join(servers))
        else:
            answer_message = "\nСписок серверов с тревогой:\n    ОК!"
        urls = db.url_list_with_alarm("url".split())
        if urls:
            answer_message += "\nСписок url с тревогой:\n    " + \
                ("\n    ".join(['url: ' + str(u) for u in urls]))
        else:
            answer_message += "\nСписок url с тревогой:\n    ОК!"
        await message.reply(answer_message, disable_web_page_preview=True)
    else:
        await message.reply('У вас не достаточно прав.')


@dp.message_handler(commands=['subscribe'])
async def add_user(message: types.Message):
    """Добавляет нового пользователя"""
    await message.reply('Добавление в базу данных...')
    await asyncio.sleep(1)

    add_users.add_user(str(message.from_user.first_name),
                       str(message.from_user.last_name),
                       str(message.from_user.username),
                       str(message.from_user.id))
    answer_message = (
        "Вы подписались на сообщения.")
    await message.reply(answer_message)


@dp.message_handler(commands=['fix'])
async def fix_url_server(message: types.Message):
    """ Убираем статус тревоги """
    if db.access_check_admin(str(message.from_user.id)):
        arguments = message.get_args()
        if str(arguments) == '':
            await message.reply('Введите url или server\n/fix vk.com username@0.0.0.0')
        else:
            arguments = arguments.split()
            await message.reply('Выключаем статусы тревоги...')
            await asyncio.sleep(1)
            for argument in arguments:
                if '@' in argument:
                    host = argument.split('@')[1]
                    if db.check_if_exist_server(host):
                        db.set_alarm_false_server(host)
                        await message.reply('Сервер {} - починен'.format(argument))
                    else:
                        await message.reply('Сервера {} нет в базе данных'.format(argument))
                else:
                    if db.check_if_exist_url(argument):
                        db.set_alarm_false_url(argument)
                        await message.reply('URL {} - починен'.format(argument), disable_web_page_preview=True)
                    else:
                        await message.reply('URL {} нет в базе данных'.format(argument), disable_web_page_preview=True)
    else:
        await message.reply('У вас не достаточно прав')


async def periodic(sleep_for): # NOQA [C901]
    while True:
        await asyncio.sleep(sleep_for)

        """ Проверка доступности сайтов """

        urls = Urls()
        urls = urls.get_all_urls()
        pool = ThreadPool(len(urls))

        old_urls_443 = pool.map(getcode200.check_443, urls)
        old_urls_80 = pool.map(getcode200.check_80, urls)

        pool.close()
        pool.join()

        new_urls_80 = []
        new_urls_443 = []
        for url_80, url_443, url in zip(old_urls_80, old_urls_443, urls):
            if 'Error' in url_443 or 'False' in url_443:
                new_urls_443.append(url + ' - ' + url_443)
                db.set_alarm_url(url)
            if 'Error' in url_80 or 'False' in url_80:
                new_urls_80.append(url + ' - ' + url_80)
                db.set_alarm_url(url)

        users = ChatUsers()
        names, surnames, usernames, chat_ids = users.get_all_chat_users_with_sub()
        for chat_id in chat_ids:
            if (db.access_check_collegue(str(chat_id)) or db.access_check_admin(str(chat_id))):
                if new_urls_80 != []:
                    answer_80 = 'ALARM!\nНе открываются на порту 80:\n'
                    answer_80 += '\n'.join(new_urls_80)
                    bot.send_message(chat_id, answer_80, disable_web_page_preview=True)
                if new_urls_443 != []:
                    answer_443 = 'ALARM!\nНе открываются на порту 443:\n'
                    answer_443 += '\n'.join(new_urls_443)
                    bot.send_message(chat_id, answer_443, disable_web_page_preview=True)

        """ Проверяем ssl """

        urls = Urls()
        urls = urls.get_all_urls()

        await asyncio.sleep(1)
        data_3 = check_ssl_cirt(urls)

        valid_list = list(map(list, zip(urls, data_3)))

        await asyncio.sleep(1)
        reply = ''
        for j in valid_list:
            if 'invalid' in j[1]:
                db.set_alarm_url(j[0])
                reply += '{}'.format(j[0] + ', ssl: ' + j[1] + '\nPlease, update this url\n')
                users = ChatUsers()
                names, surnames, usernames, chat_ids = users.get_all_chat_users_with_sub()
                for chat_id in chat_ids:
                    if (db.access_check_collegue(str(chat_id)) or db.access_check_admin(str(chat_id))):
                        await bot.send_message(chat_id, reply, disable_notification=True)

        """ Проверяем сервера """

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
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            host_temp = hosts[i]
            username_temp = usernames[i]
            if '-----BEGIN' in keys[i]:
                pr_key_temp = keys[i]
                pr_key_temp = pr_key_temp[1:-1]
                pr_key_temp = StringIO(pr_key_temp)
                privkey = paramiko.RSAKey.from_private_key(pr_key_temp)
            else:
                pr_key_temp = "src/bot/db/" + keys[i]
                try:
                    privkey = paramiko.RSAKey.from_private_key_file(pr_key_temp)
                except SSHException:
                    privkey = paramiko.DSSKey.from_private_key_file(pr_key_temp)
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
                reply = """{}@{}\nCRITICAL! LOW MEMORY!\n{}% Used\n{}Gb Avaible""".format(
                    username_temp,
                    host_temp,
                    pcent_num,
                    mem_avail_gb_num)
                users = ChatUsers()
                names, surnames, usernames, chat_ids = users.get_all_chat_users_with_sub()
                for chat_id in chat_ids:
                    if (db.access_check_collegue(str(chat_id)) or db.access_check_admin(str(chat_id))):
                        await bot.send_message(chat_id, reply, disable_notification=True)
}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic(poll))
    executor.start_polling(dp)
