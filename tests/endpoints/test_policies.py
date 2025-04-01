from datetime import (
    datetime,
    timedelta,
)

import pytest

from app.models.policy import Policy
from app.schemas.policy import FilteredPoliciesResponse
from tests.factories import (
    PolicyFactory,
    PremiumFactory,
)


@pytest.mark.anyio
async def test_get_all_policies(api_base_url, client):
    response = await client.get(f"{api_base_url}/policies")
    assert response.status_code == 200
    rsp = response.json()
    rsp_model_instance = FilteredPoliciesResponse(**rsp)
    assert isinstance(rsp_model_instance, FilteredPoliciesResponse)


@pytest.mark.anyio
async def test_get_single_policy(api_base_url, client, policy_number):
    response = await client.get(f"{api_base_url}/policies/{policy_number}")
    assert response.status_code == 200
    rsp = response.json()
    rsp_model_instance = Policy(**rsp)
    assert isinstance(rsp_model_instance, Policy)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "expiration_date, effective_date, expected",
    [
        (datetime.now() + timedelta(days=10), datetime.now(), 201),
        (datetime.now() + timedelta(days=365), datetime.now(), 201),
    ],
)
async def test_create_policy(
    api_base_url, client, policy_number, expiration_date, effective_date, expected
):
    payload = PolicyFactory.build(
        expiration_date=expiration_date,
        effective_date=effective_date,
        policy_number=policy_number,
        premium=PremiumFactory.build(amount=100.0),
    )
    response = await client.post(
        f"{api_base_url}/policies", content=payload.model_dump_json()
    )
    assert response.status_code == expected
