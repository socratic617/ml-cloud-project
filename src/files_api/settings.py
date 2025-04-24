from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class Settings(BaseSettings):
    """Settings for the files API.

    Pydantic BaseSettings doc: https://docs.pydantic.dev/latest/concepts/pydantic_settings/#installation
    FASTAPI guide to managing settings: https://fastapi.tiangolo.com/advanced/settings/
    """
    s3_bucket_name: str = Field(...)

    model_config = SettingsConfigDict(
        case_sensitive=False
    )