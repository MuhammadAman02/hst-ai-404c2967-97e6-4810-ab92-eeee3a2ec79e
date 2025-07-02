"""Application Configuration"""

import os
from typing import Optional

class Settings:
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Apple Store")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./apple_store.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # File Upload
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "static/images/products")
    
    # Store Settings
    STORE_NAME: str = os.getenv("STORE_NAME", "Apple Store")
    STORE_TAGLINE: str = os.getenv("STORE_TAGLINE", "Think Different")
    CURRENCY: str = os.getenv("CURRENCY", "USD")
    TAX_RATE: float = float(os.getenv("TAX_RATE", "0.08"))

settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)