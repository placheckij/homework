from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app.db.models.address_dbo import AddressDBO
from app.db.models.person_dbo import PersonDBO
from app.db.models.policy_dbo import PolicyDBO
from app.models.policy import Policy
from app.models.premium import Premium


class PolicyDBOFactory(SQLAlchemyFactory[PolicyDBO]): ...


class PersonDBOFactory(SQLAlchemyFactory[PersonDBO]): ...


class AddressDBOFactory(SQLAlchemyFactory[AddressDBO]): ...


class PolicyFactory(ModelFactory[Policy]): ...


class PremiumFactory(ModelFactory[Premium]): ...
