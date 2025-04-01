from typing import (
    Any,
    Generator,
)

import pytest
from asgi_lifespan import LifespanManager
from httpx import (
    ASGITransport,
    AsyncClient,
)
from pytest_mock import MockerFixture

from tests.fake_db import (
    AsyncDBApiMock,
    test_policy_number,
)


@pytest.fixture(scope="session")
def policy_number():
    yield test_policy_number


@pytest.fixture(scope="session")
def api_base_url():
    return "/task/api/v1"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def async_db_api_mock() -> Generator[AsyncDBApiMock, Any, Any]:
    yield AsyncDBApiMock()


@pytest.fixture(scope="session")
async def client(
    async_db_api_mock: AsyncDBApiMock,
    session_mocker: MockerFixture,
):
    session_mocker.patch(
        "app.api.deps.async_db_api", new_callable=lambda: async_db_api_mock
    )
    session_mocker.patch(
        "app.db.async_db_api.AsyncDBApi", new_callable=lambda: async_db_api_mock
    )
    from app.main import app

    async with LifespanManager(app, startup_timeout=30, shutdown_timeout=30):
        async with AsyncClient(  # noqa S113
            transport=ASGITransport(app=app), base_url="http://localhost"
        ) as ac:
            yield ac
