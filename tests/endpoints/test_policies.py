import pytest

from app.models.policy import Policy
from app.schemas.policy import AllPoliciesResponse


@pytest.mark.anyio
async def test_get_all_policies(api_base_url, client):
    response = await client.get(f"{api_base_url}/policies")
    assert response.status_code == 200
    rsp = response.json()
    rsp_model_instance = AllPoliciesResponse(root=rsp)
    assert isinstance(rsp_model_instance, AllPoliciesResponse)


@pytest.mark.anyio
async def test_get_single_policy(api_base_url, client, policy_number):
    response = await client.get(f"{api_base_url}/policies/{policy_number}")
    assert response.status_code == 200
    rsp = response.json()
    rsp_model_instance = Policy(**rsp)
    assert isinstance(rsp_model_instance, Policy)
