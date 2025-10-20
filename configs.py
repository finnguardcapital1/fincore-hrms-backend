from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./fincore.db"
    SECRET_KEY: str = "change_me"
    JWT_EXPIRY_HOURS: int = 8

settings = Settings()
