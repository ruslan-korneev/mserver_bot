"""Работа с url"""
from typing import Dict, List, NamedTuple

from common import db


# noinspection PyCompatibility
class Url(NamedTuple):
    """Структура Url"""
    url: str
    alarm_status: bool


class Urls:
    def __init__(self):
        self._urls = self._load_urls()
        self._urls_with_alarm = self._load_urls_with_alarm

    @staticmethod
    def _load_urls() -> List[Url]:
        """Возвращает список url из БД"""
        urls = db.url_list("url".split())
        return urls

    def get_all_urls(self) -> List[Dict]:
        """Возвращает список url."""
        return self._urls

    def _load_urls_with_alarm(self) -> List[Url]:
        """Возвращает список url из БД"""
        return db.url_list_with_alarm("url".split())

    def get_all_urls_with_alarm(self) -> List[Dict]:
        """Возвращает список url."""
        return self._urls_with_alarm

    def set_alarm_url(self, host):
        """Устанавливаем флаги тревоги"""
        db.set_alarm_url(host)
