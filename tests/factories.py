from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory

from app.db.models.address_dbo import AddressDBO
from app.db.models.person_dbo import PersonDBO
from app.db.models.policy_dbo import PolicyDBO


class PolicyDBOFactory(SQLAlchemyFactory[PolicyDBO]): ...


class PersonDBOFactory(SQLAlchemyFactory[PersonDBO]): ...


class AddressDBOFactory(SQLAlchemyFactory[AddressDBO]): ...
