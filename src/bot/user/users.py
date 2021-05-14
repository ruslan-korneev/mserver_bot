"""Работа с пользователями"""
from typing import Dict, List, NamedTuple

from common import db


# noinspection PyCompatibility
class ChatUser(NamedTuple):
    """Структура пользователей"""
    name: str
    surname: str
    username: str
    chat_id: str
    subscribe: bool


class ChatUsers:
    def __init__(self):
        self._names, self._surnames, self._usernames = self._load_chat_users()
        (
            self._names_sub,
            self._surnames_sub,
            self._usernames_sub,
            self._chat_id_sub) = self._load_chat_users_with_sub()

    @staticmethod
    def _load_chat_users() -> List[ChatUser]:
        """Возвращает список пользователей из БД"""
        return db.user_list("name surname username".split())

    @staticmethod
    def _load_chat_users_with_sub() -> List[ChatUser]:
        """Возвращает список пользователей с подпиской из БД"""
        return db.user_list_with_sub("name surname username chat_id".split())

    def get_all_chat_users(self) -> List[Dict]:
        """Возвращает список пользователей."""
        return self._names, self._surnames, self._usernames

    def get_all_chat_users_with_sub(self) -> List[Dict]:
        """Возвращает список пользователей с подпиской."""
        return (
            self._names_sub,
            self._surnames_sub,
            self._usernames_sub,
            self._chat_id_sub)
