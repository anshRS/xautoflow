import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET")
    REDIRECT_URL: str = os.getenv("REDIRECT_URL")

settings = Settings()
