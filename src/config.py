from functools import lru_cache
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for the app.
    """
    app_name: str
    app_description: str | None

    # authentication
    secret_key: str
    jwt_algorithm: str
    jwt_access_token_expires_minutes: int
    jwt_refresh_token_expires_days: int

    # DB parameters
    DB_HOST: str
    DB_PORT: str | int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_DRIVER_SYNC: str
    DB_DRIVER_ASYNC: str

    # postgres params
    POSTGRES_DB: str = 'postgres'
    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'admin'

    # redis params
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ''
    REDIS_PREFIX: str = ''
    REDIS_MAX_CONNECTIONS: int = 10
    REDIS_MIN_CONNECTIONS: int = 1
    REDIS_MAX_IDLE_TIME: int = 60
    REDIS_MAX_ACTIVE_TIME: int = 60
    REDIS_CONNECTION_TIMEOUT: int = 10

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+{self.DB_DRIVER_ASYNC}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SYNC_DATABASE_URL(self):
        return f"postgresql+{self.DB_DRIVER_SYNC}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class ProductionSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".prod.env")


class DevelopmentSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".dev.env")
        print(env_file)


class TestingSettings(Settings):
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), ".test.env")


@lru_cache
def get_settings():
    """
    Get the settings from the environment.
    """
    mode = os.getenv("API_MODE")
    if mode in ("test", "testing"):
        return TestingSettings()
    if mode in ("dev", "development"):
        return DevelopmentSettings()
    if mode in ("prod", "production"):
        return ProductionSettings()
    return DevelopmentSettings()


settings = get_settings()