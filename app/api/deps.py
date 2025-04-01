from app.core.config import (
    Settings,
    settings,
)
from app.db.async_db_api import AsyncDBApi

async_db_api = AsyncDBApi(
    db_server=settings.DB_HOST,
    database=settings.DB_INSTANCE_NAME,
    user_name=settings.DB_USER,
    password=settings.DB_PASSWD,
)


def get_db() -> AsyncDBApi:
    return async_db_api


def get_settings() -> Settings:
    return settings
