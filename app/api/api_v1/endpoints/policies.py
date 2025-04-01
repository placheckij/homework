import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api import deps
from app.models.policy import Policy
from app.schemas.HttpError import HTTPError
from app.schemas.policy import AllPoliciesResponse

LOG = logging.getLogger(__name__)


router = APIRouter()


@router.get(
    "/policies",
    status_code=status.HTTP_200_OK,
    summary="Get all policies",
    response_model=AllPoliciesResponse,
)
async def get_all_policies(
    *,
    async_db_api: deps.AsyncDBApi = Depends(deps.get_db),
):
    try:
        policies = await async_db_api.get_all_policies()
    except Exception as e:
        LOG.error(f"Error getting policies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return AllPoliciesResponse([policy.to_model() for policy in policies])


@router.get(
    "/policies/{policy_number}",
    status_code=status.HTTP_200_OK,
    summary="Get single policy",
    responses={
        404: {
            "model": HTTPError,
            "description": "Policy not found",
        }
    },
    response_model=Policy,
)
async def get_single_policy(
    *,
    policy_number: str,
    async_db_api: deps.AsyncDBApi = Depends(deps.get_db),
):
    try:
        policy = await async_db_api.get_single_policy_by_number(policy_number)
    except Exception as e:
        LOG.error(f"Error getting policies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    if policy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Policy with number {policy_number} not found",
        )
    return policy.to_model()


@router.post(
    "/policies",
    status_code=status.HTTP_201_CREATED,
    summary="Create policy",
    responses={
        422: {
            "model": HTTPError,
            "description": "Validation error",
        }
    },
)
async def create_policy():
    pass
