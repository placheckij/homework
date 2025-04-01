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
        self.create_insurance_policy = AsyncMock()
        some_policy = PolicyDBOFactory.build(
            policy_number=test_policy_number,
            created_at=int(datetime.now().timestamp()),
            effective_date=int(datetime.now().timestamp()),
            expiration_date=int((datetime.now() + timedelta(days=365)).timestamp()),
            policyholder=PersonDBOFactory.build(
                date_of_birth=int(datetime.fromisoformat("1980-01-01").timestamp()),
                email="test@test.pl",
                address=AddressDBOFactory.build(),
            ),
        )
        self.get_all_policies = AsyncMock(return_value=[some_policy])
        self.get_single_policy_by_number = AsyncMock(return_value=some_policy)
        self.get_engine = MagicMock()
