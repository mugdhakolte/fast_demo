import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

logger = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    logger.info("Loading Config settings from the environment...")
    return Settings()
