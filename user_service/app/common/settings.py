from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    BOOK_SERVICE_URI: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
print(settings.DB_URL)
print(settings.BOOK_SERVICE_URI)