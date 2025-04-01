from datetime import date

from pydantic import (
    BaseModel,
    EmailStr,
)

from app.models.address import Address


class Person(BaseModel):
    id_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone: str
    address: Address
