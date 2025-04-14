import os
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Open WebUI Agent Service"
    description: str = "Agent service for Open WebUI"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Agent settings
    enable_code_execution: bool = os.getenv("ENABLE_CODE_EXECUTION", "False").lower() == "true"
    code_execution_engine: str = os.getenv("CODE_EXECUTION_ENGINE", "jupyter")
    code_execution_jupyter_url: str = os.getenv("CODE_EXECUTION_JUPYTER_URL", "http://localhost:8888")
    
    enable_code_interpreter: bool = os.getenv("ENABLE_CODE_INTERPRETER", "False").lower() == "true"
    code_interpreter_engine: str = os.getenv("CODE_INTERPRETER_ENGINE", "jupyter")
    code_interpreter_jupyter_url: str = os.getenv("CODE_INTERPRETER_JUPYTER_URL", "http://localhost:8888")
    
    enable_tools: bool = os.getenv("ENABLE_TOOLS", "True").lower() == "true"
    tool_server_connections: Dict[str, Any] = {}
    
    # Task settings
    task_model: str = os.getenv("TASK_MODEL", "gpt-3.5-turbo")
    task_model_external: bool = os.getenv("TASK_MODEL_EXTERNAL", "False").lower() == "true"
    
    # Inference service URL
    inference_service_url: str = os.getenv("INFERENCE_SERVICE_URL", "http://inference-service:8001")
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"


settings = Settings()
