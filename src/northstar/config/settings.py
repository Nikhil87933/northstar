from pydantic import AnyHttpUrl, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_host: str = Field(validation_alias="NORTHSTAR_POSTGRES_HOST")
    postgres_port: int = Field(
        default=5432,
        validation_alias="NORTHSTAR_POSTGRES_PORT",
        gt=0,
        le=65535,
    )
    postgres_database: str = Field(
        validation_alias="NORTHSTAR_POSTGRES_DATABASE",
        min_length=1,
    )
    postgres_username: str = Field(
        validation_alias="NORTHSTAR_POSTGRES_USERNAME",
        min_length=1,
    )
    postgres_password: SecretStr = Field(
        validation_alias="NORTHSTAR_POSTGRES_PASSWORD",
    )

    api_base_url: AnyHttpUrl = Field(validation_alias="NORTHSTAR_API_BASE_URL")
    files_base_url: AnyHttpUrl = Field(validation_alias="NORTHSTAR_FILES_BASE_URL")

    environment: str = Field(
        default="development",
        validation_alias="NORTHSTAR_ENVIRONMENT",
    )
    log_level: str = Field(
        default="INFO",
        validation_alias="NORTHSTAR_LOG_LEVEL",
    )
