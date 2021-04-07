""" Работа с url — их добавление, удаление"""
from typing import NamedTuple, Optional

from common import db


# noinspection PyCompatibility
class Message(NamedTuple):
    """Структура распаршенного сообщения о новом url"""
    url: str


# noinspection PyCompatibility
class AddUrl(NamedTuple):
    """Структура добавленного в БД нового url"""
    ident: Optional[int]
    url: str
    alarm_status: bool


def add_url(url: str) -> AddUrl:
    """Добавляет нового url.
    Принимает на вход url, пришедшего в бот."""
    db.insert("urls", {
        "url": url,
        "alarm_status": True,
    })
    return AddUrl(ident=None,
                  url=url,
                  alarm_status=True)


def del_url(url: str) -> None:
    """Удаляет url по его url"""
    db.delete_url("urls", url)
