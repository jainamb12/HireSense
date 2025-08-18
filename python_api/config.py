from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    mongo_details: str
    backend_url: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()