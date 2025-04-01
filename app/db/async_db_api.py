import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db import Base
from app.db.models.person_dbo import PersonDBO
from app.db.models.policy_dbo import PolicyDBO
from app.db.models.premium_dbo import PremiumDBO

LOG = logging.getLogger(__name__)


class AsyncDBApi:
    def __init__(self, db_server: str, database: str, user_name: str, password: str):
        self._db_server = db_server
        self._database = database
        self._username = user_name
        self._password = password
        self._engine = None
        self._async_session = None
        self._configs = {}

    async def connect(self) -> None:
        sqlalchemy_database_uri = f"postgresql+asyncpg://{self._username}:{self._password}@{self._db_server}/{self._database}"
        try:
            self._engine = create_async_engine(
                sqlalchemy_database_uri,
                pool_recycle=3600,
                connect_args={"server_settings": {"jit": "off"}},
                pool_pre_ping=True,
            )
        except Exception as e:
            LOG.error(f"DB engine creation error: {e}.")
        try:
            self._async_session = async_sessionmaker(
                self._engine,
                expire_on_commit=False,
                class_=AsyncSession,
                join_transaction_mode="rollback_only",
            )
        except Exception as e:
            LOG.error(f"Creating an async_sessionmaker failed: {e}.")

    async def close(self) -> None:
        if self._engine:
            await self._engine.dispose()

    async def create_all(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def create_insurance_policy(
        self, policy_data: dict, person_data: dict, premium_data: dict
    ):
        try:
            async with self._async_session() as session:
                # Create the related objects
                person = PersonDBO(**person_data)
                premium = PremiumDBO(**premium_data)

                # Create the policy with relationships
                policy = PolicyDBO(
                    policy_id=policy_data["policy_id"],
                    type=policy_data["type"],
                    status=policy_data["status"],
                    created_at=policy_data["created_at"],
                    effective_date=policy_data["effective_date"],
                    expiration_date=policy_data["expiration_date"],
                    notes=policy_data.get("notes"),
                    policyholder=person,  # Direct assignment creates relationship
                    premium=premium,  # Direct assignment creates relationship
                )

                # Add only the parent
                session.add(policy)
                # No need for explicit commit with context manager

                # Refresh to get generated IDs if needed
                await session.commit(policy)
        except SQLAlchemyError as e:
            raise e
        else:
            return policy

    async def get_all_policies(self) -> list[PolicyDBO]:
        try:
            async with self._async_session() as session:
                stmt = select(PolicyDBO)
                result = await session.execute(stmt)
                policies = result.scalars().all()
        except SQLAlchemyError as e:
            raise e
        else:
            return policies

    async def get_single_policy_by_number(self, policy_number: str) -> PolicyDBO:
        try:
            async with self._async_session() as session:
                stmt = select(PolicyDBO).where(PolicyDBO.policy_number == policy_number)
                result = await session.execute(stmt)
                policy = result.scalars().first()
        except SQLAlchemyError as e:
            raise e
        else:
            return policy

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is not initialized.")
        return self._engine
