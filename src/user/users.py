"""Работа с пользователями"""
from typing import Dict, List, NamedTuple

from common import db


# noinspection PyCompatibility
class ChatUser(NamedTuple):
    """Структура пользователей"""
    chat_id: str
    subscribe: bool


class ChatUsers:
    def __init__(self):
        self._chat_users = self._load_chat_users()
        self._chat_users_with_sub = self._load_chat_users_with_sub()

    @staticmethod
    def _load_chat_users() -> List[ChatUser]:
        """Возвращает список пользователей из БД"""
        chat_users = db.user_list("chat_id".split())
        return chat_users

    @staticmethod
    def _load_chat_users_with_sub() -> List[ChatUser]:
        """Возвращает список пользователей из БД"""
        chat_users = db.user_list_with_sub("chat_id".split())
        return chat_users

    def get_all_chat_users(self) -> List[Dict]:
        """Возвращает список пользователей."""
        return self._chat_users

    def get_all_chat_users_with_sub(self) -> List[Dict]:
        """Возвращает список пользователей."""
        return self._chat_users_with_sub
