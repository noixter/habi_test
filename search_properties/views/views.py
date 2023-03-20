from dataclasses import asdict
from typing import Any, Callable, Optional

from search_properties.database.connector import DBConnector
from search_properties.exceptions import MethodNotAllowed
from search_properties.repositories.property_repository import (
    PropertyReadRepository,
)
from search_properties.repositories.user_repository import UserReadRepository
from search_properties.services import commands
from search_properties.views.base_views import WebServices


class PropertyView(WebServices):
    def __init__(
        self,
        request: dict[str, Any],
        db: Optional[DBConnector] = None,
        user_repo: Optional[UserReadRepository] = None,
        actions: dict[str, Callable] = None,
    ):
        super().__init__(request, db, user_repo)
        self.property_repo = PropertyReadRepository(self.db)
        self.actions = actions or {}

    def get(self):
        if not self.method == "GET":
            raise MethodNotAllowed(f"method {self.method} not allowed")

        cmd = commands.GetProperties()

        if self.params:
            cmd.property_filter = self.params

        handler = self.actions.get(type[cmd.__class__])
        if not handler:
            return []

        response = handler(self.property_repo, cmd)
        return self.serialize_response(response)

    def serialize_response(self, response: list) -> list[str, Any]:
        response = list(map(asdict, response))
        return response
