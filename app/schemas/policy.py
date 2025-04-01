from pydantic import BaseModel

from app.models.policy import Policy


class FilteredPoliciesResponse(BaseModel):
    policies: list[Policy]
    total_count: int
