import logging
from functools import lru_cache

from pydantic_settings import BaseSettings

logger = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)


@lru_cache()
async def get_settings() -> BaseSettings:
    logger.info("Loading Config settings from the environment...")
    return Settings()
