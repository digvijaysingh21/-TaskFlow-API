from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "TAaskFlow API"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    #Celery
    CELERY_BROKER_URL : str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND : str = "redis://localhost:6379/2"


    class Config:
        env_file = "../.env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()

