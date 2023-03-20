from dataclasses import dataclass
from typing import Optional

from _decimal import Decimal


@dataclass
class Status:
    name: str
    label: str


@dataclass
class Property:
    id: int
    address: str
    city: str
    price: Decimal
    description: Optional[str]
    year: Optional[int]
    status: Optional[Status] = None


@dataclass
class User:
    username: str
    password: str
