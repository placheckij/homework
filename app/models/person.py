from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    field_serializer,
)

from app.models.address import Address


class Person(BaseModel):
    id_number: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    email: EmailStr
    phone: str
    address: Address

    @field_serializer("date_of_birth", when_used="unless-none")
    def serialize_datetime(v: datetime) -> str:
        return v.isoformat()
