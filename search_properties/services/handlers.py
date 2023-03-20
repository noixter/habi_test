from typing import Optional

from search_properties.repositories.models import Property
from search_properties.repositories.property_repository import (
    PropertyReadRepository,
)
from search_properties.services.commands import GetProperties


def get_properties(
    properties_repo: PropertyReadRepository, cmd: GetProperties
) -> Optional[list[Property]]:
    properties = properties_repo.get_properties_and_status(
        filters=cmd.property_filter
    )
    if not properties:
        return []

    return properties
