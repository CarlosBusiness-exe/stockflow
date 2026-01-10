from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    DB_URL: str
    JWT_SECRET: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive=True
    )

settings: Settings = Settings()