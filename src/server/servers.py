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

    def _load_servers(self) -> List[Server]:
        """Возвращает список серверов из БД"""
        servers = db.fetchall("servers", "username host path_to_key".split())
        return servers

    def get_all_servers(self) -> List[Dict]:
        """Возвращает список серверов."""
        return self._servers
