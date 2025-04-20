from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, DirectoryPath

class Settings(BaseSettings):
    PROJECT_NAME: str = "FinSight Agent"
    API_V1_STR: str = "/api/v1"
    API_KEY: str = "development_key"  # Default value for development
    
    DATABASE_URL: PostgresDsn
    GEMINI_API_KEY: str
    EXTERNAL_MARKET_DATA_API_URL: str
    EXTERNAL_MARKET_DATA_API_KEY: Optional[str] = None
    EXTERNAL_NEWS_API_URL: str
    EXTERNAL_NEWS_API_KEY: Optional[str] = None
    LOCAL_KB_PATH: DirectoryPath

    # Yahoo Finance Endpoints
    YAHOO_QUOTE_ENDPOINT: str = "/v6/finance/quote"
    YAHOO_CHART_ENDPOINT: str = "/v8/finance/chart"
    YAHOO_SUMMARY_ENDPOINT: str = "/v11/finance/quoteSummary"
    YAHOO_AUTOCOMPLETE_ENDPOINT: str = "/v6/finance/autocomplete"
    YAHOO_MARKET_SUMMARY_ENDPOINT: str = "/v6/finance/quote/marketSummary"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields

settings = Settings()