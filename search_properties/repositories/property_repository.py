from dataclasses import fields
from typing import Any, Optional, Union

from search_properties.database.connector import DBConnector
from search_properties.database.mysql_connector import MYSQLConnector
from search_properties.repositories import sql
from search_properties.repositories.models import Property, Status
from search_properties.repositories.repository import ReadRepository


class PropertyReadRepository(ReadRepository[Property]):
    model_fields: set[str]
    excluded_fields: set[str]

    def __init__(self, db: Optional[DBConnector] = None):
        self.db = db or MYSQLConnector()
        self.model = Property.__name__.lower()
        self.model_fields = {
            f"{self.model}.{field.name}" for field in fields(Property)
        }

    def get(self, id_: Union[str, int]) -> Property:
        property_ = self.db.select(
            table=self.model, filters={f"{self.model}.id": id_}
        )
        return self.to_domain(property_) if property_ else None

    def all(
        self,
        filters: dict[str, str] = None,
        order_by: list[str] = None,
    ) -> Optional[list[Property]]:
        properties = self.db.select(
            table=self.model,
            filters=filters,
            order_by=order_by,
        )
        return (
            [self.to_domain(property_) for property_ in properties]
            if properties
            else None
        )

    def get_properties_and_status(
        self,
        filters: dict[str, str] = None,
        order_by: list[str] = None,
    ) -> list[Property]:
        properties = self.db.select(
            base_query=sql.PROPERTIES_AND_STATUS,
            filters=filters,
            order_by=order_by,
        )
        return (
            [self.to_domain(property_) for property_ in properties]
            if properties
            else None
        )

    def to_domain(self, row: dict[str, Any]) -> Property:
        return Property(
            id=row.get("id"),
            address=row.get("address"),
            city=row.get("city"),
            price=row.get("price"),
            description=row.get("description"),
            year=row.get("year"),
            status=Status(
                name=row.get("status_name"), label=row.get("status_label")
            ),
        )
