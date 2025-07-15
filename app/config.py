from functools import lru_cache
import json
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Bot(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="BOT_",
        extra="ignore",
    )

    token: str
    admins: list[int]

    @field_validator("admins")
    def parse_json_list(cls, value: Any) -> list[int]:
        """Parse JSON string to list of integers"""
        return json.loads(value) if isinstance(value, str) else value


class DB(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        extra="ignore",
    )

    is_enabled: bool
    host: str
    port: int
    name: str
    user: str
    password: str


class Payments(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PAYMENTS_",
        extra="ignore",
    )

    token: str


class Config:
    bot: Bot = Bot()  # type: ignore
    payments: Payments = Payments()  # type: ignore
    db: DB = DB()  # type: ignore


@lru_cache
def load_config():
    return Config()
