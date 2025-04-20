import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

class Settings:
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XAutoFlow"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    EXTERNAL_MARKET_DATA_API_URL: str = os.getenv("EXTERNAL_MARKET_DATA_API_URL")
    EXTERNAL_MARKET_DATA_API_KEY: str = os.getenv("EXTERNAL_MARKET_DATA_API_KEY")
    EXTERNAL_NEWS_API_URL: str = os.getenv("EXTERNAL_NEWS_API_URL")
    EXTERNAL_NEWS_API_KEY: str = os.getenv("EXTERNAL_NEWS_API_KEY")
    
    # Local Knowledge Base
    LOCAL_KB_PATH: str = os.getenv("LOCAL_KB_PATH", "./local_kb")

settings = Settings()
