from pydantic import RootModel

from app.models.policy import Policy


class AllPoliciesResponse(RootModel[list[Policy]]):
    root: list[Policy]
