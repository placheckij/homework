import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import (
    FastAPI,
    status,
)
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import command
from alembic import config as alembic_config
from app.api.api_v1 import api_router
from app.api.deps import get_db
from app.core.config import settings
from app.db.async_db_api import AsyncDBApi

LOG = logging.getLogger(__name__)


async def run_migrations(engine: AsyncEngine):
    alembic_cfg = alembic_config.Config("alembic.ini")

    url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWD}@{settings.DB_HOST}/{settings.DB_INSTANCE_NAME}"
    alembic_cfg.set_main_option("sqlalchemy.url", url)

    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: alembic_cfg.attributes.__setitem__(
                "connection", sync_conn
            )
        )
        await conn.run_sync(lambda sync_conn: command.upgrade(alembic_cfg, "head"))


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Setup
    LOG.info(f"Backend version: {settings.BACKEND_VERSION}")
    async_db_api: AsyncDBApi = get_db()
    await async_db_api.connect()
    await async_db_api.create_all()
    LOG.info("Running alembic upgrade head")
    try:
        await run_migrations(async_db_api.get_engine())
    except Exception as e:
        LOG.exception(f"Error running migrations: {e}")
    LOG.info("Migrations complete")

    # Run
    yield

    # Teardown
    await async_db_api.close()


app = FastAPI(
    title="Homework task",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    version=settings.BACKEND_VERSION,
)

app.include_router(api_router, prefix=settings.API_V1_STR)  # <----- API versioning

from fastapi.middleware.cors import CORSMiddleware  # noqa E402

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/task/api/v1/status", status_code=status.HTTP_200_OK, summary="Health check")
async def healthcheck() -> dict:
    return {"msg": "OK"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    LOG.error(f"Validation error, request: {request}, error: {exc.errors()}")
    return {"detail": exc.errors(), "body": exc.body}


if __name__ == "__main__":
    # Use this for debugging purposes only
    from dotenv import load_dotenv

    load_dotenv()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="debug")  # noqa S104
