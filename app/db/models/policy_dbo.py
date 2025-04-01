import logging
import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    BigInteger,
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
    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    effective_date: Mapped[int] = mapped_column(BigInteger, nullable=False)
    expiration_date: Mapped[int] = mapped_column(BigInteger, nullable=False)
    policyholder_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("person.id"), nullable=False
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    policyholder: Mapped[PersonDBO] = relationship("PersonDBO")
    premium: Mapped[PremiumDBO] = relationship(
        "PremiumDBO", cascade="all, delete-orphan", uselist=False
    )

    def to_model(self) -> Policy:
        logging.info(f"exp date: {(datetime.fromtimestamp(self.expiration_date),)}")
        return Policy(
            policy_number=self.policy_number,
            type=self.type,
            status=self.status,
            created_at=datetime.fromtimestamp(self.created_at),
            effective_date=datetime.fromtimestamp(self.effective_date),
            expiration_date=datetime.fromtimestamp(self.expiration_date),
            policyholder=self.policyholder.to_model() if self.policyholder else None,
            premium=self.premium.to_model() if self.premium else None,
            notes=self.notes,
        )
