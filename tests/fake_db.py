from datetime import (
    datetime,
    timedelta,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
)

from tests.factories import (
    AddressDBOFactory,
    PersonDBOFactory,
    PolicyDBOFactory,
)

test_policy_number = "TestPolicy123"


class AsyncDBApiMock:
    def __init__(self):
        self.close = AsyncMock()
        self.connect = AsyncMock()
        self.create_all = AsyncMock()
        some_policy = PolicyDBOFactory.build(
            policy_number=test_policy_number,
            created_at=datetime.now(),
            effective_date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=365),
            policyholder=PersonDBOFactory.build(
                date_of_birth=datetime.fromisoformat("1980-01-01"),
                email="test@test.pl",
                address=AddressDBOFactory.build(),
            ),
        )
        self.get_policies_filtered_with_pagination = AsyncMock(
            return_value=(
                [some_policy.to_model()],
                1,
            )
        )
        self.create_insurance_policy = AsyncMock()
        self.get_all_policies = AsyncMock(return_value=[some_policy])
        self.get_single_policy_by_number = AsyncMock(return_value=some_policy)
        self.get_engine = MagicMock()
