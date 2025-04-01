import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    BigInteger,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db import Base
from app.db.models.address_dbo import AddressDBO
from app.models.person import Person


class PersonDBO(Base):
    __tablename__ = "person"
    __table_args__ = {}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    id_number: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text, nullable=False)
    last_name: Mapped[str] = mapped_column(Text, nullable=False)
    date_of_birth: Mapped[int] = mapped_column(BigInteger, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(Text, nullable=False)

    address: Mapped["AddressDBO"] = relationship("AddressDBO")

    def to_model(self) -> Person:
        return Person(
            id_number=self.id_number,
            first_name=self.first_name,
            last_name=self.last_name,
            date_of_birth=datetime.fromtimestamp(self.date_of_birth),
            email=self.email,
            phone=self.phone,
            address=self.address.to_model(),
        )
