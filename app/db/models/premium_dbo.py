import uuid

from sqlalchemy import (
    UUID,
    BigInteger,
    Enum,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db import Base
from app.models.enums import (
    PaymentFrequency,
    PaymentMethod,
)
from app.models.premium import Premium


class PremiumDBO(Base):
    __tablename__ = "premium"
    __table_args__ = {}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    frequency: Mapped[PaymentFrequency] = mapped_column(
        Enum(PaymentFrequency), nullable=False
    )
    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=False)
    next_payment_date: Mapped[int] = mapped_column(BigInteger, nullable=True)
    policy_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("policy.id"), nullable=False
    )

    def to_model(self) -> Premium:
        return Premium(
            amount=self.amount,
            frequency=self.frequency,
            method=self.method,
            next_payment_date=self.next_payment_date,
        )
