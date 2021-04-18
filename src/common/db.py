import logging
import os

from typing import Dict, List

import psycopg2


logging.basicConfig(filename="db.log", level=logging.DEBUG,
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
    query = "SELECT chat_id FROM bot_chat_user WHERE chat_id={}".format(values[0])
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    if values[0] in str(rows):
        query = """
        UPDATE bot_chat_user
        SET subscribe=TRUE
        WHERE chat_id={};
        """.format(values[0])
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, connection)
    else:
        query = """
        INSERT INTO bot_chat_user (chat_id, subscribe)
        VALUES ({}, {})
        """.format(values[0], values[1])
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, connection)


def insert_url(value: str):
    query = "INSERT INTO bot_url (url, alarm_status) VALUES ('{}', FALSE)".format(value)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def user_list(columns: List[str]):
    query = "SELECT chat_id FROM bot_chat_user"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        for index, column in enumerate(columns):
            result.append(row[index])
    return result


def user_list_with_sub(columns: List[str]):
    query = "SELECT chat_id FROM bot_chat_user WHERE subscribe=TRUE"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        for index, column in enumerate(columns):
            result.append(row[index])
    return result


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


def keys_list(columns: List[str]):
    query = "SELECT path_to_key FROM bot_server"
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        for index, column in enumerate(columns):
            result.append(row[index])
    return result


def unsubscribe(chat_id: str) -> None:
    query = """
    UPDATE bot_chat_user
    SET subscribe=FALSE
    WHERE chat_id={};
    """.format(chat_id)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(query, connection)


def delete_user(chat_id: str) -> None:
    query = """
    DELETE FROM bot_chat_user
    WHERE chat_id={}
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
