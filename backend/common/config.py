import os
from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class ServiceConfig(BaseModel):
    """Base configuration for all services"""
    service_name: str
    version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./webui.db")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "0"))
    
    # API settings
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    jwt_expires_in: int = int(os.getenv("JWT_EXPIRES_IN", "30"))  # days
    
    # Service-specific settings
    service_settings: Dict[str, Any] = {}
    
    class Config:
        env_file = ".env"


def get_service_config(service_name: str, service_settings: Optional[Dict[str, Any]] = None) -> ServiceConfig:
    """Get the configuration for a specific service"""
    config = ServiceConfig(
        service_name=service_name,
        debug=os.getenv("DEBUG", "False").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./webui.db"),
        database_pool_size=int(os.getenv("DATABASE_POOL_SIZE", "0")),
        api_prefix=os.getenv("API_PREFIX", "/api/v1"),
        cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        jwt_expires_in=int(os.getenv("JWT_EXPIRES_IN", "30")),
    )
    
    if service_settings:
        config.service_settings = service_settings
    
    return config
