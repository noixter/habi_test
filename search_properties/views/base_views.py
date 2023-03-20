from abc import ABC
from typing import Any, Callable, Optional

from search_properties.database.connector import DBConnector
from search_properties.database.mysql_connector import MYSQLConnector
from search_properties.exceptions import NotAuthenticated
from search_properties.repositories.repository import ReadRepository
from search_properties.repositories.user_repository import UserReadRepository
from search_properties.services.commands import Command


class WebServices(ABC):
    """Simil to a class based view"""

    url: str
    params: dict[str, Any] = dict()
    headers: dict[str, Any] = dict()
    allowed_methods = set(
        "options"
    )  # necessary for http initial validation response
    actions: dict[str, Callable[[ReadRepository, Command], list[dict]]]

    def __init__(
        self,
        request: dict[str, Any],
        db: Optional[DBConnector] = None,
        user_repo: Optional[UserReadRepository] = None,
    ):
        self.db = db or MYSQLConnector()
        self.user_repo = user_repo or UserReadRepository(self.db)
        self.authentication = self._authentication(request.get("Authentication"))
        self.method = request.get("method")
        self._process_service(request.get("resource"))
        self.headers = request.get("headers")

    def _authentication(self, authentication_header: dict[str, str]):
        """
        Small authentication implementation, it is only to represent
        an authentication state and does not respect any authz
        or authn politic
        :param authentication_header:
        :return:
        """
        _user = self.user_repo.get_by_username(
            username=authentication_header.get("username")
        )
        if not _user:
            raise NotAuthenticated("Invalid Credentials")

        if not _user.password == authentication_header.get("password"):
            raise NotAuthenticated("Invalid Credentials")

        self.user = _user

    def _process_service(self, resource: str):
        # Does not take in count any of the uri unicode
        # to extract the query_params

        try:
            url, _params = resource.split("?")
        except ValueError:
            url = resource
            _params = None

        if _params:
            params = _params.split("&")

            for param in params:
                key, value = param.split("=")
                self.params[key] = value

        self.url = url

    def register_action(self, cmd: str, handler: Callable):
        self.actions[cmd] = handler

    def serialize_response(self, response: list) -> dict[str, Any]:
        raise NotImplementedError()
