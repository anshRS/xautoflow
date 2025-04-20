from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, DirectoryPath

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinSight Agent"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: PostgresDsn
    GEMINI_API_KEY: str
    EXTERNAL_MARKET_DATA_API_URL: str
    EXTERNAL_MARKET_DATA_API_KEY: Optional[str] = None
    EXTERNAL_NEWS_API_URL: str
    EXTERNAL_NEWS_API_KEY: Optional[str] = None
    LOCAL_KB_PATH: DirectoryPath

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()