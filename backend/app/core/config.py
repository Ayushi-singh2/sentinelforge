from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration.
    """

    # Application
    app_name: str = "SentinelForge"

    debug: bool = False


    # API Security
    api_key: str = "sentinelforge-secret-key"


    # RAG / ChromaDB
    chroma_db_path: str = "./chroma_db"

    collection_name: str = "sentinelforge"

    # compatibility with index.py
    chroma_collection_name: str = "sentinelforge"


    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"


    # Retrieval limits
    max_top_k: int = 20


    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()