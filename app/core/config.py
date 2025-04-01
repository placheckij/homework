from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from app.utils import get_version_from_pyproject


class Settings(BaseSettings):
    # Application specific
    API_V1_STR: str = "/task/api/v1"
    BACKEND_VERSION: str = get_version_from_pyproject()

    # Database related
    DB_HOST: str
    DB_INSTANCE_NAME: str
    DB_USER: str
    DB_PASSWD: str

    # Pydantic basesettings configuration
    model_config = ConfigDict(case_sensitive=True)


settings = Settings()
