import os
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Open WebUI Retrieval Service"
    description: str = "Retrieval service for Open WebUI"
    version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # CORS settings
    cors_origins: List[str] = ["*"]
    
    # Vector database settings
    vector_db: str = os.getenv("VECTOR_DB", "chroma")
    vector_db_url: str = os.getenv("VECTOR_DB_URL", "")
    vector_db_api_key: str = os.getenv("VECTOR_DB_API_KEY", "")
    
    # Embedding settings
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_engine: str = os.getenv("EMBEDDING_ENGINE", "")
    embedding_batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "32"))
    
    # RAG settings
    enable_rag_hybrid_search: bool = os.getenv("ENABLE_RAG_HYBRID_SEARCH", "True").lower() == "true"
    enable_rag_local_web_fetch: bool = os.getenv("ENABLE_RAG_LOCAL_WEB_FETCH", "True").lower() == "true"
    enable_rag_web_search: bool = os.getenv("ENABLE_RAG_WEB_SEARCH", "True").lower() == "true"
    rag_web_search_engine: str = os.getenv("RAG_WEB_SEARCH_ENGINE", "duckduckgo")
    rag_web_search_result_count: int = int(os.getenv("RAG_WEB_SEARCH_RESULT_COUNT", "3"))
    
    # Web search API keys
    brave_search_api_key: str = os.getenv("BRAVE_SEARCH_API_KEY", "")
    serper_api_key: str = os.getenv("SERPER_API_KEY", "")
    serply_api_key: str = os.getenv("SERPLY_API_KEY", "")
    serpapi_api_key: str = os.getenv("SERPAPI_API_KEY", "")
    serpstack_api_key: str = os.getenv("SERPSTACK_API_KEY", "")
    searchapi_api_key: str = os.getenv("SEARCHAPI_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    jina_api_key: str = os.getenv("JINA_API_KEY", "")
    bing_search_api_key: str = os.getenv("BING_SEARCH_API_KEY", "")
    exa_api_key: str = os.getenv("EXA_API_KEY", "")
    perplexity_api_key: str = os.getenv("PERPLEXITY_API_KEY", "")
    kagi_search_api_key: str = os.getenv("KAGI_SEARCH_API_KEY", "")
    mojeek_search_api_key: str = os.getenv("MOJEEK_SEARCH_API_KEY", "")
    bocha_search_api_key: str = os.getenv("BOCHA_SEARCH_API_KEY", "")
    google_pse_api_key: str = os.getenv("GOOGLE_PSE_API_KEY", "")
    google_pse_engine_id: str = os.getenv("GOOGLE_PSE_ENGINE_ID", "")
    
    # File upload settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"


settings = Settings()
