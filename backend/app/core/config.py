from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for SentinelForge.

    Values can be provided through environment variables
    or a .env file.
    """

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    app_name: str = "SentinelForge"

    app_version: str = "0.1.0"

    debug: bool = False


    # --------------------------------------------------
    # API
    # --------------------------------------------------

    api_prefix: str = "/api"

    host: str = "127.0.0.1"

    port: int = 8000


    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    embedding_model: str = "all-MiniLM-L6-v2"

    chroma_db_path: str = "./chroma_db"

    chroma_collection_name: str = "sentinelforge"

    default_top_k: int = 5

    max_top_k: int = 20


    # --------------------------------------------------
    # Security
    # --------------------------------------------------

    max_query_length: int = 2000


    # --------------------------------------------------
    # Environment configuration
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached application settings instance.
    """

    return Settings()


settings = get_settings()