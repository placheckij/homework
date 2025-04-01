import uuid

from sqlalchemy import (
    UUID,
    Float,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db import Base
from app.models.coverage import Coverage


class CoverageDBO(Base):
    __tablename__ = "coverage"
    __table_args__ = {}

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    limit: Mapped[float] = mapped_column(Float, nullable=True)
    deductible: Mapped[float] = mapped_column(Float, nullable=False)
    exclusions: Mapped[list] = mapped_column(JSONB, nullable=False)

    def to_model(self) -> Coverage:
        return Coverage(
            type=self.type,
            description=self.description,
            limit=self.limit,
            deductible=self.deductible,
            exclusions=self.exclusions,
        )
