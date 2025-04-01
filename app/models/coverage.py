from pydantic import (
    BaseModel,
    Field,
)


class Coverage(BaseModel):
    type: str
    description: str
    limit: float
    deductible: float
    exclusions: list[str] = Field(default_factory=list)
