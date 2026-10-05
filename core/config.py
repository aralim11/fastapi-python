from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
        )

settings = Settings()