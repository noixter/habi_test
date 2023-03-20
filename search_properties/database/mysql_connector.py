import logging
from dataclasses import dataclass, field
from typing import Any, Optional, Union

import mysql.connector
from mysql.connector import MySQLConnection

from search_properties import config
from search_properties.database.connector import DBConnector
from search_properties.database.constants import DBTypes

logger = logging.getLogger(__name__)


@dataclass
class Join:
    table1: str
    table2: str
    column1: Optional[str] = None
    column2: Optional[str] = None

    def __post_init__(self):
        if not self.column1:
            self.column1 = "id"
        if not self.column2:
            self.column2 = "id"

    def __repr__(self):
        return (
            f"JOIN {self.table1} on "
            f"{self.table1}.{self.column1} = "
            f"{self.table2}.{self.column2} "
        )


@dataclass
class Query:
    table: Optional[str] = None
    base_query: Optional[str] = None
    columns: Optional[Union[list[str], str]] = None
    where: Optional[dict[str]] = None
    order_by: Optional[list[str]] = None
    joins: Optional[list[Join]] = field(default_factory=list)
    limit: Optional[str] = None

    def __post_init__(self):
        if not self.table and not self.base_query:
            raise ValueError("at least either table or base_query are needed")

        if not self.columns:
            self.columns = "*"
        else:
            self.columns = ",".join(self.columns)

    def get_query(self) -> str:
        repr_ = self.base_query
        if not repr_:
            repr_ = f"SELECT {self.columns} from {self.table} "
            for join in self.joins:
                repr_ += repr(join) + " "

        if self.where:
            filters_query = "AND ".join(
                [f'{key} = "{value}"' for key, value in self.where.items()]
            )
            repr_ += f"WHERE {filters_query} "
        if self.order_by:
            ordering = list(
                map(
                    lambda order: order.replace("-", "") + " DESC"
                    if order.startswith("-")
                    else order,
                    self.order_by,
                )
            )
            repr_ += f'ORDER BY {"".join(ordering)} '
        if self.limit:
            repr_ += f"LIMIT {self.limit}"
        return repr_


class MYSQLConnector(DBConnector):
    _context: MySQLConnection
    _type = DBTypes.MySQL

    def __init__(self, dictionary: Optional[bool] = None):
        self._setup()
        self.dictionary = dictionary or True

    def _setup(self) -> None:
        try:
            self._context = mysql.connector.connect(**config["DATABASE"])
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
