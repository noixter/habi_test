from typing import Optional

import pytest

from search_properties.repositories.property_repository import (
    PropertyReadRepository,
)
from search_properties.services import commands, handlers
from search_properties.services.commands import Command


class TestGetPropertiesHandler:
    properties_repo = PropertyReadRepository()

    def _execute_service(self, cmd: Optional[Command] = None):
        return handlers.get_properties(
            properties_repo=self.properties_repo,
            cmd=cmd or commands.GetProperties(),
        )

    def test_get_properties_successfully(self):
        properties = self._execute_service()
        assert properties
        assert len(properties) > 1
        for property_ in properties:
            if property_.status:
                assert property_.status.name
                assert property_.status.label

    @pytest.mark.parametrize(
        "filters",
        (
            {"property.year": 2000, "property.city": "bogota"},
            {"property.city": "medellin", "property.price": 210_000_000},
            {"property.city": "pereira"},
            {"status.name": "en_venta"},
            {"status.name": "pre_venta"},
            {"status.name": "vendido"},
            {"property.year": 2000, "status.name": "pre_venta"},
        ),
    )
    def test_get_properties_filter_property(self, filters):
        cmd = commands.GetProperties(property_filter=filters)
        properties = self._execute_service(cmd)
        assert len(properties) >= 1
        for property_ in properties:
            for key, value in filters.items():
                field, accessor = key.split(".")
                # validates if there nested objects
                if hasattr(property_, field):
                    # brings the nested object
                    object_ = getattr(property_, field)
                    # accessor is an attr of nested object
                    assert getattr(object_, accessor) == value
                    continue
                assert getattr(property_, accessor) == value

    @pytest.mark.parametrize("filters", ({"status.name": "compra_venta"},))
    def test_get_properties_non_results(self, filters):
        cmd = commands.GetProperties(property_filter=filters)
        properties = self._execute_service(cmd)
        assert len(properties) == 0
