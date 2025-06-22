from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WEATHER_STACK_API_KEY: str
    model_config = SettingsConfigDict(env_file=".env.local")

settings = Settings()