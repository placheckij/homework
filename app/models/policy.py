from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_serializer,
    field_validator,
)

from app.models.coverage import Coverage
from app.models.enums import (
    PolicyStatus,
    PolicyType,
)
from app.models.person import Person
from app.models.premium import Premium


class Policy(BaseModel):
    policy_number: str
    type: PolicyType
    status: PolicyStatus = PolicyStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    effective_date: datetime
    expiration_date: datetime
    policyholder: Person
    coverages: list[Coverage] = Field(default_factory=list)
    premium: Premium | None = None
    notes: str | None = None

    @field_validator("expiration_date", mode="before")
    def expiration_after_effective(v, values: ValidationInfo):
        if (
            "effective_date" in values.data
            and datetime.fromisoformat(str(v)) <= values.data["effective_date"]
        ):
            raise ValueError("Expiration date must be after effective date")
        return v

    @field_serializer(
        "created_at", "effective_date", "expiration_date", when_used="unless-none"
    )
    def serialize_datetime(v: datetime) -> str:
        return v.isoformat()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "policy_number": "POL-12345-A",
                "type": "AUTO",
                "status": "ACTIVE",
                "effective_date": "2023-01-01",
                "expiration_date": "2024-01-01",
                "policyholder": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1980-01-01",
                    "email": "john.doe@example.com",
                    "phone": "555-123-4567",
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown",
                        "state": "CA",
                        "zip_code": "12345",
                    },
                },
                "coverages": [
                    {
                        "type": "liability",
                        "description": "Bodily injury and property damage liability",
                        "limit": 100000.00,
                        "deductible": 500.00,
                    }
                ],
                "premium": {
                    "amount": 1200.00,
                    "frequency": "MONTHLY",
                    "method": "CREDIT_CARD",
                    "next_payment_date": "2023-02-01",
                },
            }
        }
    )
