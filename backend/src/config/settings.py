import os
from dataclasses import dataclass

_DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/compliance"
)


@dataclass(frozen=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", _DEFAULT_DATABASE_URL),
    )
