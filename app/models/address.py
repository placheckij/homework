from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    state: str | None = None
    zip_code: str
    country: str
