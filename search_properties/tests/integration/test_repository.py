import mysql.connector
import pytest
from faker import Faker

from search_properties.repositories.models import Property
from search_properties.repositories.property_repository import (
    PropertyReadRepository,
)

faker = Faker()


class TestPropertyRepository:
    repository = PropertyReadRepository()

    def test_get_property(self):
        property_ = self.repository.get(id_=1)
        assert property_
        assert type(property_) == Property
        assert property_.id
        assert property_.city
        assert property_.year
        assert property_.price
        assert property_.address
        assert property_.description

    def test_get_non_existing_property(self):
        property_ = self.repository.get(id_=faker.pyint())
        assert not property_

    def test_list_properties(self):
        properties = self.repository.all()
        assert len(properties) > 1

    @pytest.mark.parametrize(
        "filters",
        (
            ({"year": 2011}),
            ({"city": "bogota"}),
            ({"year": 2000}),
            ({"city": "medellin"}),
        ),
    )
    def test_list_properties_with_filters(self, filters):
        properties = self.repository.all(filters=filters)
        year = filters.get("year")
        city = filters.get("city")
        assert len(properties) >= 1
        for property_ in properties:
            if year:
                assert property_.year == year
            if city:
                assert property_.city == city

    def test_list_properties_with_filters_no_results(self):
        properties = self.repository.all(filters={"city": "imaginary_city"})
        assert not properties

    @pytest.mark.parametrize("order_by", (["-year"], ["year"]))
    def test_list_properties_with_ordering(self, order_by):
        properties = self.repository.all(order_by=order_by)
        assert len(properties) >= 1
        years = [
            property_.year
            for property_ in properties
            if property_.year is not None
        ]

        # validates the ordering
        first_year, last_year = years[0], years[-1]
        if order_by[0].startswith("-"):
            assert first_year > last_year
        else:
            assert first_year < last_year

    def test_list_properties_with_ordering_and_filters(self):
        filters = {"city": "bogota"}
        order_by = ["-price"]
        properties = self.repository.all(filters=filters, order_by=order_by)
        prices = [
            property_.year
            for property_ in properties
            if property_.year is not None
        ]
        first_price, last_price = prices[0], prices[-1]
        assert properties
        assert len(properties) > 1
        assert first_price > last_price
        for property_ in properties:
            assert property_.city == "bogota"

    def test_list_properties_filter_does_not_exists(self):
        filters = {"status": "en_venta"}
        with pytest.raises(mysql.connector.Error) as err:
            self.repository.all(filters=filters)

        assert "Unknown column", str(err.value)

    def test_get_properties_and_status(self):
        properties = self.repository.get_properties_and_status()
        assert len(properties) > 1
        for property_ in properties:
            if property_.status:
                assert property_.status.name
                assert property_.status.label

    @pytest.mark.parametrize("status", ("en_venta", "pre_venta", "vendido"))
    def test_get_properties_and_status_filters(self, status):
        properties = self.repository.get_properties_and_status(
            filters={"status.name": status}
        )
        assert len(properties) > 1
        for property_ in properties:
            assert property_.status.name == status

    @pytest.mark.parametrize(
        "field, value",
        (
            ("property.city", "bogota"),
            ("property.year", 2011),
            ("property.price", 120_000_000),
        ),
    )
    def test_get_properties_and_status_property_filters(self, field, value):
        properties = self.repository.get_properties_and_status(
            filters={field: value}
        )
        assert len(properties) > 1
        for property_ in properties:
            if hasattr(property_, field.split(".")[0]):
                assert getattr(property_, field) == value
