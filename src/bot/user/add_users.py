""" Работа с пользователями — их добавление, удаление"""
from typing import NamedTuple, Optional

from common import db


# noinspection PyCompatibility
class Message(NamedTuple):
    """Структура распаршенного сообщения о новом пользователе"""
    name: str
    surname: str
    username: str
    chat_id: str
    subscribe: bool


# noinspection PyCompatibility
class AddUser(NamedTuple):
    """Структура добавленного в БД нового пользователя"""
    ident: Optional[int]
    name: str
    surname: str
    username: str
    chat_id: str
    subscribe: bool


def add_user(name: str, surname: str, username: str, chat_id: str) -> AddUser:
    """Добавляет нового пользователя.
    Принимает на вход идентификатор пользователя, пришедшего в бот."""
    db.insert_user({
        "name": name,
        "surname": surname,
        "username": username,
        "chat_id": chat_id,
        "subscribe": True,
    })
    return AddUser(ident=None,
                   name=name,
                   surname=surname,
                   username=username,
                   chat_id=chat_id,
                   subscribe=True)


def unsubscribe(chat_id: str) -> None:
    """Удаляет пользователя по его chat id"""
    db.unsubscribe(chat_id)


def delete_user(chat_id: str) -> None:
    """Удаляет пользователя по его chat id"""
    db.delete_user(chat_id)
