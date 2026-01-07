from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str
    DR_URL: str

    model_config = SettingsConfigDict(
        env_files = ".env",
        case_sensitive=True
    )

settings: Settings = Settings()