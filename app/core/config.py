from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()
env.read_env()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str

    SECRET_KEY: str
    ALGO: str


settings = Settings()
