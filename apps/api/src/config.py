# Checks if theere is the env file and if DATABASE_URL and REDIS_URL exists.
# If they do not exist. This will immidiately crash.

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
            env_file = ".env"

settings = Settings()