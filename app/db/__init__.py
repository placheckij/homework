from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RecordAlreadyExistsError(Exception):
    pass
