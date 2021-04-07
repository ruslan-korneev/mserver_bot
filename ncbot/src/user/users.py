"""Работа с пользователями"""
from typing import Dict, List, NamedTuple

from common import db


# noinspection PyCompatibility
class User(NamedTuple):
    """Структура пользователей"""
    chat_id: str
    subscribe: bool


class Users:
    def __init__(self):
        self._users = self._load_users()

    @staticmethod
    def _load_users() -> List[User]:
        """Возвращает список пользователей из БД"""
        users = db.fetchall("user", "chat_id subscribe".split())
        return users

    def get_all_users(self) -> List[Dict]:
        """Возвращает список пользователей."""
        return self._users
