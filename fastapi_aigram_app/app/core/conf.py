from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DEBUG: bool
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    BOT_TOKEN: str
    WB_URL: str
    INTERVAL: str

    @property
    def ASYNC_DATABASE_URL(self):
        """Путь для асинхронного подключения SQLAlchemy к PostgreSQL."""
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB_NAME}"
        )

    @property
    def SYNC_DATABASE_URL(self):
        """Путь для синхронного подключения APScheduler к PostgreSQL."""
        return (
            "postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB_NAME}"
        )

    class Config:
        env_file = f'{BASE_DIR.parent}.env'


settings = Settings()
