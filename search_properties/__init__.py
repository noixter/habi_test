from dataclasses import dataclass
from decouple import config


@dataclass
class DBConfig:
    user: str
    password: str
    database: str
    host: str
    port: str


@dataclass
class Config:
    database: DBConfig


config = Config(
    database=DBConfig(
        user=config('DB_USER', 'admin'),
        password=config('DB_PASSWORD', 'password'),
        database=config('DB_NAME', 'habi_test'),
        host=config('DB_HOST', 'localhost'),
        port=config('DB_PORT', '3309'),
    )
)
