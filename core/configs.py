from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str
    DB_URL: str

    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://usuario:senha@localhost:5432/banco_padrao"

    model_config = SettingsConfigDict(
        env_files = ".env",
        case_sensitive=True
    )

settings: Settings = Settings()