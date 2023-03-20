from dataclasses import dataclass
from typing import Any


class Command:
    pass


@dataclass
class GetProperties(Command):
    property_filter: dict[str, Any] = None
