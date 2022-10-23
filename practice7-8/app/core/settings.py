from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    POSTGRES_DSN: str
    
    APP_HOST: Optional[str] = '0.0.0.0'
    APP_PORT: Optional[int] = 8080


settings = Settings()