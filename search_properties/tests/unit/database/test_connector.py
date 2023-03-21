import mysql.connector
import pytest
from faker import Faker

from search_properties import config
from search_properties.database.constants import DBTypes
from search_properties.database.mysql_connector import MYSQLConnector

faker = Faker()


class TestMySQLDBConnector:
    connector = MYSQLConnector()

    def test_create_connection(self):
        assert self.connector.connected
        assert self.connector._type == DBTypes.MySQL

    def test_create_connection_failed_by_credentials(
        self,
    ):
        config.database.password = faker.pystr()
        with pytest.raises(mysql.connector.Error) as err:
            MYSQLConnector()

        assert "Access denied" in str(err.value)

    def test_disconnect(self):
        self.connector.disconnect()
        assert not self.connector.connected
        with pytest.raises(mysql.connector.Error):
            self.connector.select(table_name="property")
