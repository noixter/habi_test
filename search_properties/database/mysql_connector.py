import logging
from dataclasses import asdict
from typing import Any, Optional, Union

import mysql.connector
from mysql.connector import MySQLConnection

from search_properties import config
from search_properties.database.connector import DBConnector
from search_properties.database.constants import DBTypes
from search_properties.database.models import Query

logger = logging.getLogger(__name__)


class MYSQLConnector(DBConnector):
    _context: MySQLConnection
    _type = DBTypes.MySQL

    def __init__(self, dictionary: Optional[bool] = None):
        self._setup()
        self.dictionary = dictionary or True

    def _setup(self) -> None:
        try:
            self._context = mysql.connector.connect(
                **asdict(config.database)
            )
            self.connected = self._context.is_connected()
        except mysql.connector.Error as err:
            logger.exception(err.errno)
            raise

    def select(self, *args, **kwargs) -> Optional[Union[list[dict], dict]]:
        with self._context.cursor(
            buffered=True, dictionary=self.dictionary
        ) as cursor:
            _query = Query(
                base_query=kwargs.get("base_query"),
                columns=kwargs.get("columns"),
                table=kwargs.get("table"),
                where=kwargs.get("filters"),
                order_by=kwargs.get("order_by"),
                joins=kwargs.get("joins", []),
                limit=kwargs.get("limit"),
            )

            try:
                cursor.execute(_query.get_query())
                return (
                    cursor.fetchall()
                    if cursor.rowcount > 1
                    else cursor.fetchone()
                )
            except mysql.connector.Error as err:
                logger.exception(err.errno)
                raise

    def insert(self, table_name: str, params: dict[str, Any]) -> None:
        with self._context.cursor(dictionary=self.dictionary) as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} ({','.join(params.keys())}) "
                    f"VALUES {','.join(params.values())}"
                )
                self._context.commit()
            except mysql.connector.Error as err:
                logger.exception(err.errno)
                raise

    def disconnect(self) -> None:
        self._context.close()
        self.connected = False
