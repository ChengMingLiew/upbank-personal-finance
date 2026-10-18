# Checks if theere is the env file and if DATABASE_URL and REDIS_URL exists.
# If they do not exist. This will immidiately crash.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    REDIS_URL: str
    ENCRYPTION_KEY: str

settings = Settings()