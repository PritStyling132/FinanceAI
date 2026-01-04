from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Alpha Vantage
    alpha_vantage_api_key: str = ""

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "financial_knowledge"

    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"

    # Application
    debug: bool = True
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
