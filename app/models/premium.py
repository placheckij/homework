from datetime import date

from pydantic import (
    BaseModel,
    field_validator,
)

from app.models.enums import (
    PaymentFrequency,
    PaymentMethod,
)


class Premium(BaseModel):
    amount: float
    frequency: PaymentFrequency
    method: PaymentMethod
    next_payment_date: date

    @field_validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Payment amount must be positive")
        return v
