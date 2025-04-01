import logging
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.exc import IntegrityError

from app.api import deps
from app.models.enums import (
    PolicyStatus,
    PolicyType,
)
from app.models.policy import Policy
from app.schemas.HttpError import HTTPError
from app.schemas.policy import FilteredPoliciesResponse

LOG = logging.getLogger(__name__)


router = APIRouter()


@router.get(
    "/policies",
    status_code=status.HTTP_200_OK,
    summary="Get all policies",
    response_model=FilteredPoliciesResponse,
)
async def get_policies_filtered_with_pagination(
    *,
    async_db_api: deps.AsyncDBApi = Depends(deps.get_db),
    expiration_date_from: datetime = Query(
        alias="expiration-date-from",
        default=None,
        description="Expiration date from which to filter policies",
    ),
    expiration_date_to: datetime = Query(
        alias="expiration-date-to",
        default=None,
        description="Expiration date to which to filter policies",
    ),
    effective_date_from: datetime = Query(
        alias="effective-date-from",
        default=None,
        description="Effective date from which to filter policies",
    ),
    effective_date_to: datetime = Query(
        alias="effective-date-to",
        default=None,
        description="Effective date to which to filter policies",
    ),
    page: int = Query(
        alias="page", default_factory=lambda: 1, description="Page number"
    ),
    page_size: int = Query(
        alias="page-size", default_factory=lambda: 10, description="Page size"
    ),
    policyholder_id_number: str = Query(
        alias="policyholder-id-number",
        default=None,
        description="Policyholder ID number to filter by",
    ),
    policy_number: str = Query(
        alias="policy-number", default=None, description="Policy number to filter by"
    ),
    policy_status: PolicyStatus = Query(
        alias="policy-status", default=None, description="Policy status to filter by"
    ),
    policy_type: PolicyType = Query(
        alias="policy-type", default=None, description="Policy type to filter by"
    ),
):
    try:
        (
            policies,
            total_count,
        ) = await async_db_api.get_policies_filtered_with_pagination(
            expiration_date_from=expiration_date_from,
            expiration_date_to=expiration_date_to,
            effective_date_from=effective_date_from,
            effective_date_to=effective_date_to,
            page=page,
            page_size=page_size,
            policy_number=policy_number,
            policyholder_id_number=policyholder_id_number,
            policy_type=policy_type,
            policy_status=policy_status,
        )
    except Exception as e:
        LOG.error(f"Error getting policies: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    return FilteredPoliciesResponse(policies=policies, total_count=total_count)


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
async def create_policy(
    *,
    policy_request: Policy,
    async_db_api: deps.AsyncDBApi = Depends(deps.get_db),
):
    try:
        await async_db_api.create_insurance_policy(policy_request)
    except IntegrityError as e:
        LOG.error(f"Policy creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Policy {policy_request.policy_number} already exists",
        )
    except Exception as e:
        LOG.error(f"Policy creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
