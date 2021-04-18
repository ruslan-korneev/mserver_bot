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

    @staticmethod
    def _load_urls() -> List[Url]:
        """Возвращает список url из БД"""
        urls = db.url_list("url".split())
        return urls

    def get_all_urls(self) -> List[Dict]:
        """Возвращает список url."""
        return self._urls
