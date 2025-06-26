# app/settings/base.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

ENV_FILE = ".env"


class RedisSettings(BaseSettings):
    url: str = Field(default="redis://localhost:6379/0")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="allow",
    )


class AdminSettings(BaseSettings):
    username: str = Field(default="admin")
    password: SecretStr = Field(default="admin")
    secret_key: SecretStr = Field(default="")
    token_expire_minutes: int = Field(default=30)  # Tiempo de expiración del token
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ADMIN_",
        extra="allow",
    )


class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite+aiosqlite:///./sql_app.db")
    sync_url: str = Field(default="sqlite:///./sql_app.db")
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="DATABASE_",
        extra="allow",
    )


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    admin: AdminSettings = AdminSettings()
    api_key: SecretStr = Field(default="supersecretkey123")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


settings = Settings()
