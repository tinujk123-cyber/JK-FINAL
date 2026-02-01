"""
Configuration module for JK TRINETRA FastAPI Backend.

Loads settings from environment variables with validation.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    environment: str = "development"
    
    # Convex Integration
    convex_url: str = "https://neat-crow-934.convex.cloud"
    convex_site_url: str = "https://neat-crow-934.convex.site"
    webhook_secret: str = "development-secret"
    
    # Yahoo Finance Settings
    yahoo_cache_ttl_seconds: int = 60
    yahoo_history_period: str = "1y"
    
    # Rate Limiting
    max_concurrent_scans: int = 10
    scan_delay_ms: int = 100
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
        "https://neat-crow-934.convex.site",
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to avoid re-reading environment on every call.
    """
    return Settings()


# Convenience export
settings = get_settings()
