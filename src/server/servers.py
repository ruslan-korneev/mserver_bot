"""Работа с серверами"""
from typing import Dict, List, NamedTuple

from common import db


class Server(NamedTuple):
    """Структура серверов"""
    host: str
    username: str
    path_to_key: int
    alarm_status: bool


class Servers:
    def __init__(self):
        self._servers = self._load_servers()
        self._servers_with_alarm = self._load_servers_with_alarm()

    def _load_servers(self) -> List[Server]:
        """Возвращает список серверов из БД"""
        servers = db.server_list("username host".split())
        return servers

    def _load_servers_with_alarm(self) -> List[Server]:
        """Возвращает список серверов из БД"""
        servers = db.server_list_with_alarm("username host".split())
        return servers

    def get_all_servers(self) -> List[Dict]:
        """Возвращает список серверов."""
        return self._servers

    def get_all_servers_with_alarm(self) -> List[Dict]:
        """Возвращает список серверов."""
        return self._servers_with_alarm

    def set_alarm_server(self, host):
        """Устанавливаем флаги тревоги"""
        db.set_alarm_server(host)


class Keys:
    def __init__(self):
        self._keys = self._load_keys()

    def _load_keys(self) -> List[Server]:
        """ Возвращает список ключей от серверов из БД """
        keys = db.keys_list("path_to_key".split())
        return keys

    def get_all_keys(self) -> List[Dict]:
        """ Возвращает список ключей от серверов """
        return self._keys
