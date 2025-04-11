import os
from typing import List, Dict, Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Open WebUI Inference Service"
    description: str = "Inference service for Open WebUI"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Ollama settings
    enable_ollama_api: bool = True
    ollama_base_urls: List[str] = ["http://localhost:11434"]
    ollama_api_configs: Dict[str, Any] = {}
    
    # OpenAI settings
    enable_openai_api: bool = True
    openai_api_base_urls: List[str] = ["https://api.openai.com/v1"]
    openai_api_keys: List[str] = []
    openai_api_configs: Dict[str, Any] = {}
    
    # Direct connections
    enable_direct_connections: bool = False
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"


settings = Settings()
