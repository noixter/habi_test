from dataclasses import fields
from typing import Any, Optional

from search_properties.database.connector import DBConnector
from search_properties.database.mysql_connector import MYSQLConnector
from search_properties.repositories.models import User
from search_properties.repositories.repository import _M, ReadRepository


class UserReadRepository(ReadRepository[User]):
    def __init__(self, db: Optional[DBConnector] = None):
        self.db = db or MYSQLConnector()
        self.model = (
            f"auth_{User.__name__.lower()}"  # fixed for django auth_model
        )
        self.model_fields = {
            f"{self.model}.{field.name}" for field in fields(User)
        }

    def get_by_username(self, username: str) -> Optional[User]:
        user = self.db.select(
            table=self.model, filters={f"{self.model}.username": username}
        )
        return self.to_domain(user) if user else None

    def get(self, filters: Optional[dict] = None) -> Optional[User]:
        user = self.db.select(table=self.model, filters=filters)
        return self.to_domain(user) if user else None

    def all(
        self,
        filters: Optional[dict[str, str]] = None,
        order_by: Optional[list[str]] = None,
    ) -> Optional[list[_M]]:
        # No needed to this implementation
        raise NotImplementedError

    def to_domain(self, row: dict[str, Any]) -> User:
        return User(username=row.get("username"), password=row.get("password"))
