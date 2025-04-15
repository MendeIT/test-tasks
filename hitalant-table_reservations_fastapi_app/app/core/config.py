from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Настройки приложения."""
    BASE_DIR: ClassVar = Path(__file__).resolve().parent.parent.parent

    DEBUG: bool
    TIMEZONE: str

    UVICORN_HOST: str
    UVICORN_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / '.env'),
        env_file_encoding='utf-8'
    )

    @property
    def ASYNC_DATABASE_URL(self):
        """Путь для асинхронного подключения к PostgreSQL."""

        return (
            'postgresql+asyncpg://'
            f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/'
            f'{self.POSTGRES_DB}'
        )

    @property
    def TEST_ASYNC_DATABASE_URL(self):
        return f"{self.ASYNC_DATABASE_URL}_test"


settings = Settings()
