import os
from typing import List, Union, Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, PostgresDsn, validator, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "XAutoFlow Fintech Agent"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # LLM Configuration
    LLM_PROVIDER: str = Field("openai", description="Provider for the main LLM (e.g., 'openai', 'azure', 'ollama')")
    OPENAI_API_KEY: Optional[str] = Field(None, description="OpenAI API Key")
    AZURE_OPENAI_ENDPOINT: Optional[str] = Field(None, description="Azure OpenAI Endpoint")
    AZURE_OPENAI_API_KEY: Optional[str] = Field(None, description="Azure OpenAI API Key")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, description="Anthropic API Key")
    OLLAMA_BASE_URL: Optional[AnyHttpUrl] = Field(None, description="Base URL for Ollama API")
    LLM_MODEL_NAME: str = Field("gpt-4o", description="Name of the main LLM model to use")

    # Embedding Model Configuration
    EMBEDDING_MODEL_PROVIDER: str = Field("openai", description="Provider for the embedding model")
    EMBEDDING_MODEL_NAME: str = Field("text-embedding-3-small", description="Name of the embedding model")

    # Database Configuration (Using PostgresDsn for validation)
    DATABASE_URL: PostgresDsn = Field("postgresql+asyncpg://user:password@host:port/dbname", description="Async PostgreSQL Database URL")

    # LlamaIndex Configuration
    PERSIST_DIR: str = Field("./storage", description="Directory to store LlamaIndex persistent data")
    DOCUMENTS_DIR: str = Field("./knowledge_base", description="Directory containing documents for indexing")
    CHUNK_SIZE: int = Field(512, description="Chunk size for LlamaIndex text splitting")
    CHUNK_OVERLAP: int = Field(50, description="Chunk overlap for LlamaIndex text splitting")

    # Autogen Configuration (Optional)
    # AUTOGEN_CONFIG_LIST: Optional[str] = Field(None, description="JSON string for Autogen agent configuration")

    # Security
    SECRET_KEY: str = Field("your_strong_secret_key_here", description="Secret key for JWT")
    ALGORITHM: str = Field("HS256", description="Algorithm for JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, description="Access token expiry in minutes")

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(["http://localhost:8000"], description="List of allowed CORS origins")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Tool Specific Settings
    WEB_SEARCH_MAX_RESULTS: int = Field(5, description="Maximum results for web search tool")
    ALLOWED_FILE_DIRS: List[str] = Field(["./output"], description="List of allowed directories for file I/O tool")

    @validator("ALLOWED_FILE_DIRS", pre=True)
    def assemble_allowed_dirs(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            return [os.path.abspath(i.strip()) for i in v.split(",")]
        elif isinstance(v, list):
            return [os.path.abspath(i.strip()) for i in v]
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings
settings = Settings()

# --- Helper function to get LLM configuration for Autogen/Langchain --- 

def get_llm_config() -> Dict[str, Any]:
    """Provides LLM configuration based on the loaded settings."""
    if settings.LLM_PROVIDER == "openai":
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in environment variables for OpenAI provider")
        return {
            "model": settings.LLM_MODEL_NAME,
            "api_key": settings.OPENAI_API_KEY,
            # Add other OpenAI specific params like temperature if needed
        }
    elif settings.LLM_PROVIDER == "azure":
        if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY must be set for Azure provider")
        return {
            "model": settings.LLM_MODEL_NAME,
            "api_key": settings.AZURE_OPENAI_API_KEY,
            "base_url": settings.AZURE_OPENAI_ENDPOINT,
            "api_type": "azure", # Specify API type for Langchain/Autogen if needed
            "api_version": "2023-05-15" # Example API version, adjust as needed
        }
    elif settings.LLM_PROVIDER == "anthropic":
         if not settings.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY must be set for Anthropic provider")
         # Note: Autogen/Langchain might use different keys for Anthropic
         return {
            "model": settings.LLM_MODEL_NAME,
            "anthropic_api_key": settings.ANTHROPIC_API_KEY,
         }
    elif settings.LLM_PROVIDER == "ollama":
        if not settings.OLLAMA_BASE_URL:
             raise ValueError("OLLAMA_BASE_URL must be set for Ollama provider")
        return {
            "model": settings.LLM_MODEL_NAME,
            "base_url": str(settings.OLLAMA_BASE_URL),
            # Ollama specific params might be needed here for Langchain/Autogen
        }
    # Add other providers as needed
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

# --- Helper function to get Embedding model --- 

# (Implementation depends on LlamaIndex/Langchain integration specifics)
# Example placeholder:
def get_embedding_model():
    # This function would initialize and return the appropriate embedding model
    # instance based on settings.EMBEDDING_MODEL_PROVIDER and NAME.
    # e.g., using LlamaIndex's OpenAIEmbedding, HuggingFaceEmbedding, etc.
    print(f"Placeholder: Initialize embedding model {settings.EMBEDDING_MODEL_NAME} from {settings.EMBEDDING_MODEL_PROVIDER}")
    # Replace with actual LlamaIndex/Langchain embedding model initialization
    # from llama_index.embeddings.openai import OpenAIEmbedding
    # from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    # if settings.EMBEDDING_MODEL_PROVIDER == 'openai':
    #    return OpenAIEmbedding(model=settings.EMBEDDING_MODEL_NAME, api_key=settings.OPENAI_API_KEY)
    # elif settings.EMBEDDING_MODEL_PROVIDER == 'huggingface':
    #    return HuggingFaceEmbedding(model_name=settings.EMBEDDING_MODEL_NAME)
    # ... add other providers
    return None # Placeholder 