import os
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Open WebUI Chat Service"
    description: str = "Chat service for Open WebUI"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./webui.db")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "0"))
    
    # Chat settings
    enable_chat_history: bool = True
    enable_chat_templates: bool = True
    enable_chat_export: bool = True
    enable_chat_sharing: bool = True
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_expires_in: int = int(os.getenv("JWT_EXPIRES_IN", "30"))  # days
    
    class Config:
        env_file = ".env"


settings = Settings()
