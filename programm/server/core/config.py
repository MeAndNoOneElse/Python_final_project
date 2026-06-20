from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SplitChek API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./splitchek.db"
    TELEGRAM_BOT_TOKEN: str = ""
    WEBAPP_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Разрешаем дополнительные поля из .env


settings = Settings()
