import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    DateTime,
    Enum,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db import Base
from app.db.models.person_dbo import PersonDBO
from app.db.models.premium_dbo import PremiumDBO
from app.models.enums import (
    PolicyStatus,
    PolicyType,
)
from app.models.policy import Policy


class PolicyDBO(Base):
    __tablename__ = "policy"
    __table_args__ = {}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    policy_number: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    type: Mapped[PolicyType] = mapped_column(Enum(PolicyType), nullable=False)
    status: Mapped[PolicyStatus] = mapped_column(Enum(PolicyStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    effective_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    policyholder_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("person.id"), nullable=False
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    policyholder: Mapped[PersonDBO] = relationship("PersonDBO", lazy="joined")
    premium: Mapped[PremiumDBO] = relationship(
        "PremiumDBO", lazy="joined", cascade="all, delete-orphan", uselist=False
    )

    def to_model(self) -> Policy:
        return Policy(
            policy_number=self.policy_number,
            type=self.type,
            status=self.status,
            created_at=self.created_at,
            effective_date=self.effective_date,
            expiration_date=self.expiration_date,
            policyholder=self.policyholder.to_model() if self.policyholder else None,
            premium=self.premium.to_model() if self.premium else None,
            notes=self.notes,
        )

    @classmethod
    def from_model(cls, policy: Policy) -> "PolicyDBO":
        return cls(
            policy_number=policy.policy_number,
            type=policy.type,
            status=policy.status,
            created_at=policy.created_at,
            effective_date=policy.effective_date,
            expiration_date=policy.expiration_date,
            policyholder=PersonDBO.from_model(policy.policyholder),
            notes=policy.notes,
        )
