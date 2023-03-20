from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, Union

from search_properties.database.connector import DBConnector

_M = TypeVar("_M")


class ReadRepository(ABC, Generic[_M]):
    model: str
    db: DBConnector

    @abstractmethod
    def get(self, id_: Union[str, int]) -> Optional[_M]:
        """Retrieve a unique element based on its ID"""

    @abstractmethod
    def all(
        self,
        filters: Optional[dict[str, str]] = None,
        order_by: Optional[list[str]] = None,
    ) -> Optional[list[_M]]:
        """Retrieve all the elements, query can be
        filtered or ordered
        """


class WriteRepository(ABC, Generic[_M]):
    model: str
    db: DBConnector

    @abstractmethod
    def insert(self, model: _M) -> None:
        """Creates a new row of model instance"""
