import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Open WebUI API Gateway"
    description: str = "API Gateway for Open WebUI microservices"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Service URLs
    inference_service_url: str = os.getenv("INFERENCE_SERVICE_URL", "http://inference-service:8001")
    agent_service_url: str = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8002")
    retrieval_service_url: str = os.getenv("RETRIEVAL_SERVICE_URL", "http://retrieval-service:8003")
    chat_service_url: str = os.getenv("CHAT_SERVICE_URL", "http://chat-service:8004")
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_expires_in: int = int(os.getenv("JWT_EXPIRES_IN", "30"))  # days
    
    class Config:
        env_file = ".env"


settings = Settings()
