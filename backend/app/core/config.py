"""
Application configuration and settings for O-IAxis
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Global application settings"""

    # API Configuration
    API_TITLE: str = "O-IAxis by Vrilon"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "Financial Intelligence Platform - Quantum-Ready Hybrid Infrastructure"

    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = True

    # Database Configuration
    DATABASE_URL: Optional[str] = None
    DB_ECHO: bool = False

    # Security
    SECRET_KEY: str = "o-iaxis-dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost,http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
