import logging
from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    and_,
    func,
    select,
)
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db import Base
from app.db.models.address_dbo import AddressDBO
from app.db.models.coverage_dbo import CoverageDBO
from app.db.models.person_dbo import PersonDBO
from app.db.models.policy_dbo import PolicyDBO
from app.db.models.premium_dbo import PremiumDBO
from app.models.enums import (
    PolicyStatus,
    PolicyType,
)
from app.models.policy import Policy

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

    async def create_insurance_policy(self, policy: Policy) -> None:
        try:
            async with self._async_session() as session:
                policy_dbo = PolicyDBO.from_model(policy)
                session.add(policy_dbo)
                await session.commit()
        except SQLAlchemyError as e:
            raise e
        except IntegrityError as e:
            raise e

    async def get_policies_filtered_with_pagination(
        self,
        expiration_date_from: datetime,
        expiration_date_to: datetime,
        effective_date_from: datetime,
        effective_date_to: datetime,
        page: int,
        page_size: int,
        policy_number: str | None,
        policyholder_id_number: str,
        policy_type: PolicyType | None,
        policy_status: PolicyStatus | None,
    ) -> tuple[list, int]:
        page = page - 1 if page > 0 else 0
        page_size = page_size if page_size > 0 else 10
        try:
            async with self._async_session() as session:
                count_stmt = select(func.count(PolicyDBO.id)).where(
                    and_(
                        PolicyDBO.effective_date >= effective_date_from
                        if effective_date_from is not None
                        else True,
                        PolicyDBO.effective_date <= effective_date_to
                        if effective_date_to is not None
                        else True,
                        PolicyDBO.expiration_date >= expiration_date_from
                        if expiration_date_from is not None
                        else True,
                        PolicyDBO.expiration_date <= expiration_date_to
                        if expiration_date_to is not None
                        else True,
                        PolicyDBO.policyholder.has(
                            PersonDBO.id_number == policyholder_id_number
                        )
                        if policyholder_id_number is not None
                        else True,
                        PolicyDBO.policy_number.like(f"%{policy_number}%")
                        if policy_number is not None
                        else True,
                        PolicyDBO.type == policy_type
                        if policy_type is not None
                        else True,
                        PolicyDBO.status == policy_status
                        if policy_status is not None
                        else True,
                    )
                )
                count_result = await session.execute(count_stmt)
                total_count = count_result.scalar()
                stmt = (
                    select(PolicyDBO)
                    .where(
                        and_(
                            PolicyDBO.effective_date >= effective_date_from
                            if effective_date_from is not None
                            else True,
                            PolicyDBO.effective_date <= effective_date_to
                            if effective_date_to is not None
                            else True,
                            PolicyDBO.expiration_date >= expiration_date_from
                            if expiration_date_from is not None
                            else True,
                            PolicyDBO.expiration_date <= expiration_date_to
                            if expiration_date_to is not None
                            else True,
                            PolicyDBO.policyholder.has(
                                PersonDBO.id_number == policyholder_id_number
                            )
                            if policyholder_id_number is not None
                            else True,
                            PolicyDBO.policy_number.like(f"%{policy_number}%")
                            if policy_number is not None
                            else True,
                            PolicyDBO.type == policy_type
                            if policy_type is not None
                            else True,
                            PolicyDBO.status == policy_status
                            if policy_status is not None
                            else True,
                        )
                    )
                    .order_by(PolicyDBO.created_at.desc())
                    .offset(page * page_size)
                    .limit(page_size)
                )
                result = await session.execute(stmt)
                policies: list[PolicyDBO] = result.scalars().all()
        except SQLAlchemyError as e:
            LOG.error(e)
            return [], 0
        policies = [policy.to_model() for policy in policies]
        return policies, total_count

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

    async def get_single_address(self, person_id: UUID) -> AddressDBO:
        try:
            async with self._async_session() as session:
                stmt = select(AddressDBO).where(AddressDBO.person_id == person_id)
                result = await session.execute(stmt)
                address = result.scalars().first()
        except SQLAlchemyError as e:
            raise e
        else:
            return address

    async def get_single_person(self, id_number: str) -> PersonDBO:
        try:
            async with self._async_session() as session:
                stmt = select(PersonDBO).where(PersonDBO.id_number == id_number)
                result = await session.execute(stmt)
                person = result.scalars().first()
        except SQLAlchemyError as e:
            raise e
        else:
            return person

    async def get_single_premium(self, policy_id: UUID) -> PremiumDBO:
        try:
            async with self._async_session() as session:
                stmt = select(PremiumDBO).where(PremiumDBO.policy_id == policy_id)
                result = await session.execute(stmt)
                premium = result.scalars().first()
        except SQLAlchemyError as e:
            raise e
        else:
            return premium

    async def get_coverages(self, policy_id) -> list[CoverageDBO]:
        try:
            async with self._async_session() as session:
                stmt = select(CoverageDBO).where(CoverageDBO.policy_id == policy_id)
                result = await session.execute(stmt)
                coverages = result.scalars().all()
        except SQLAlchemyError as e:
            raise e
        else:
            return coverages

    def get_engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is not initialized.")
        return self._engine
