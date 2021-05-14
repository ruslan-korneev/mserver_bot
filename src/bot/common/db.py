import logging
import os

from typing import Dict, List

import psycopg2


logging.basicConfig(filename="bot.log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


db_name = os.environ.get('POSTGRES_DB')
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_host = 'db'
db_port = '5432'

connection = psycopg2.connect(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port)


def insert_user(column_values: Dict):
    values = tuple(column_values.values())
    query = "SELECT chat_id FROM bot_chat_user WHERE chat_id='{}'".format(values[3])
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if values[3] in str(rows):
        query = """
        UPDATE bot_chat_user
        SET subscribe=TRUE
        WHERE chat_id='{}';
        """.format(values[3])
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, connection)
    else:
        query = """
        INSERT INTO bot_chat_user (username, chat_id, subscribe, name, surname, status)
        VALUES ('{}', '{}', {}, '{}', '{}', 'user')
        """.format(values[2], values[3], values[4], values[0], values[1])
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, connection)


def insert_url(value: str):
    query = "INSERT INTO bot_url (url, alarm_status) VALUES ('{}', FALSE)".format(value)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def user_list(columns: List[str]):
    query = "SELECT (name, surname, username) FROM bot_chat_user"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    names = []
    surnames = []
    usernames = []
    for r in result:
        r = r.replace('(', '')
        r = r.replace(')', '')
        names.append(r.split(',')[0])
        surnames.append(r.split(',')[1])
        usernames.append(r.split(',')[2])
    return names, surnames, usernames


def user_list_with_sub(columns: List[str]):
    query = """
    SELECT (name, surname, username, chat_id)
    FROM bot_chat_user WHERE subscribe=TRUE
    """
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    names = []
    surnames = []
    usernames = []
    chat_ids = []
    for r in result:
        r = r.replace('(', '')
        r = r.replace(')', '')
        names.append(r.split(',')[0])
        surnames.append(r.split(',')[1])
        usernames.append(r.split(',')[2])
        chat_ids.append(r.split(',')[3])
    return names, surnames, usernames, chat_ids


def url_list(columns: List[str]):
    query = "SELECT url FROM bot_url"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        for index, column in enumerate(columns):
            result.append(row[index])
    return result


def server_list(columns: List[str]):
    query = "SELECT (username, host) FROM bot_server"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    old_list = []
    for i in range(len(rows)):
        old_list.append(rows[i][0])

    new_list = []
    for l in range(len(old_list)):
        new_list.append(old_list[l][1:-1])

    result = []
    for i in range(len(new_list)):
        result.append(new_list[i].replace(',', '@'))
    return result


def server_list_with_alarm(columns: List[str]):
    query = "SELECT (username, host) FROM bot_server WHERE alarm_status=TRUE"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    old_list = []
    for i in range(len(rows)):
        old_list.append(rows[i][0])

    new_list = []
    for l in range(len(old_list)):
        new_list.append(old_list[l][1:-1])

    result = []
    for i in range(len(new_list)):
        result.append(new_list[i].replace(',', '@'))
    return result


def url_list_with_alarm(columns: List[str]):
    query = "SELECT url FROM bot_url WHERE alarm_status=TRUE"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        for index, column in enumerate(columns):
            result.append(row[index])
    return result


def keys_list(columns: List[str]):
    query = "SELECT (path_to_key, ssh_key) FROM bot_server"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for i in range(len(rows)):
        result.append(rows[i][0])
    rows, result = result, []
    for r in rows:
        r = r.replace('(', '')
        r = r.replace(')', '')
        if r.split(',')[0] == '""':
            result.append(r.split(',')[1])
        else:
            result.append(r.split(',')[0])

    return result


def unsubscribe(chat_id: str) -> None:
    query = """
    UPDATE bot_chat_user
    SET subscribe=FALSE
    WHERE chat_id='{}';
    """.format(chat_id)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def delete_user(chat_id: str) -> None:
    query = """
    DELETE FROM bot_chat_user
    WHERE chat_id='{}'
    """.format(chat_id)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def set_alarm_server(host):
    query = """
    UPDATE bot_server
    SET alarm_status=TRUE
    WHERE host='{}';
    """.format(host)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def set_alarm_url(url):
    query = """
    UPDATE bot_url
    SET alarm_status=TRUE
    WHERE url='{}';
    """.format(url)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def set_alarm_false_server(host):
    query = """
    UPDATE bot_server
    SET alarm_status=FALSE
    WHERE host='{}';
    """.format(host)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def set_alarm_false_url(url):
    query = """
    UPDATE bot_url
    SET alarm_status=FALSE
    WHERE url='{}';
    """.format(url)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def check_if_exist_server(host):
    query = """
    SELECT EXISTS(SELECT 1 FROM bot_server WHERE host = '{}');
    """.format(host)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if 'True' in str(rows):
        return True
    else:
        return False


def check_if_exist_url(url):
    query = """
    SELECT EXISTS(SELECT 1 FROM bot_url WHERE url = '{}');
    """.format(url)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if 'True' in str(rows):
        return True
    else:
        return False


def access_check_admin(chat_id):
    query = """
    SELECT status
    FROM bot_chat_user
    WHERE chat_id = '{}';
    """.format(chat_id)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if 'admin' in str(rows):
        return True
    else:
        return False


def access_check_collegue(chat_id):
    query = """
    SELECT status
    FROM bot_chat_user
    WHERE chat_id = '{}';
    """.format(chat_id)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if 'collegue' in str(rows):
        return True
    else:
        return False
