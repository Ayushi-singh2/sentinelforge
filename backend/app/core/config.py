from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration.
    """

    app_name: str = "SentinelForge"

    debug: bool = False

    # API security
    api_key: str = ""

    # RAG settings
    chroma_db_path: str = "./chroma_db"

    collection_name: str = "sentinelforge"

    embedding_model: str = "all-MiniLM-L6-v2"


    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()