import json
import os

import pytest

from search_properties.database.mysql_connector import MYSQLConnector
from search_properties.exceptions import MethodNotAllowed
from search_properties.repositories.user_repository import UserReadRepository
from search_properties.services import commands
from search_properties.services.handlers import get_properties
from search_properties.tests.conftest import TEST_DIR
from search_properties.views.views import PropertyView


def _read_requests():
    file_path = os.path.join(TEST_DIR, "data", "requests.json")
    with open(file_path, "r") as file:
        request = json.load(file)
    return request


class TestPropertyViews:
    @classmethod
    def setup_class(cls):
        cls.request = _read_requests()
        cls.db = MYSQLConnector()
        cls.user_repo = UserReadRepository()

    def test_get_view_without_filters(self):
        request = self.request.get("without_filters")
        view = PropertyView(request=request, db=self.db, user_repo=self.user_repo)
        view.register_action(
            cmd=type[commands.GetProperties], handler=get_properties
        )
        response = view.get()
        assert type(response) == list
        for element in response:
            for key in element.keys():
                if not element.get(key):
                    continue
                assert element.get(key)

    @pytest.mark.parametrize("status", ("en_venta", "pre_venta", "vendido"))
    def test_get_view_status_filter(self, status):
        request = self.request.get(status)
        view = PropertyView(request=request, db=self.db, user_repo=self.user_repo)
        view.register_action(
            cmd=type[commands.GetProperties], handler=get_properties
        )
        response = view.get()
        assert type(response) == list
        for element in response:
            assert element.get("status").get("name") == status

    def test_get_view_many_filters(self):
        requests = self.request.get("with_filters")
        for request in requests:
            view = PropertyView(
                request=request, db=self.db, user_repo=self.user_repo
            )
            view.register_action(
                cmd=type[commands.GetProperties], handler=get_properties
            )
            response = view.get()
            assert type(response) == list

    def test_unhandled_method_view(self):
        request = self.request.get("method_not_allowed")
        view = PropertyView(request=request, db=self.db, user_repo=self.user_repo)
        view.register_action(
            cmd=type[commands.GetProperties], handler=get_properties
        )
        with pytest.raises(MethodNotAllowed):
            view.get()
