from abc import ABC, abstractmethod
from typing import Any, TypeVar, Union

DB_TYPE = TypeVar("DB_TYPE", bound=str)


class DBConnector(ABC):
    _type: DB_TYPE
    connected: bool = False
    _context: Any

    @abstractmethod
    def _setup(self) -> None:
        """creates the connections with db"""

    @abstractmethod
    def select(self, *args, **kwargs) -> Union[list[dict], dict]:
        """Executes a query with statements SELECT"""

    @abstractmethod
    def insert(self, table_name: str, params: dict[str, Any]) -> None:
        """Performs an INSERT query type on db created
        :param table_name model where the object will be created
        :param params parameters to be inserted
        """

    @abstractmethod
    def disconnect(self) -> None:
        """Closes the database connection"""
