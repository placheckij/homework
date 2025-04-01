import uuid

from sqlalchemy import (
    UUID,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db import Base
from app.models.address import Address


class AddressDBO(Base):
    __tablename__ = "address"
    __table_args__ = {}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    street: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(Text, nullable=False)
    state: Mapped[str] = mapped_column(Text, nullable=True)
    zip_code: Mapped[str] = mapped_column(Text, nullable=False)
    country: Mapped[str] = mapped_column(Text, nullable=False)
    person_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("person.id"), nullable=False
    )

    def to_model(self) -> Address:
        return Address(
            street=self.street,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            country=self.country,
        )

    @classmethod
    def from_model(cls, address: Address) -> "AddressDBO":
        return cls(
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country=address.country,
        )
