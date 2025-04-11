import logging
from typing import Any

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_embedding_model():
    """
    Get the embedding model based on configuration
    """
    try:
        if settings.embedding_engine == "ollama":
            # Use Ollama for embeddings
            from app.services.embeddings_ollama import OllamaEmbeddings
            return OllamaEmbeddings(
                model=settings.embedding_model,
                batch_size=settings.embedding_batch_size,
            )
        elif settings.embedding_engine == "openai":
            # Use OpenAI for embeddings
            from app.services.embeddings_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                model=settings.embedding_model,
                batch_size=settings.embedding_batch_size,
            )
        else:
            # Use sentence-transformers for embeddings
            from sentence_transformers import SentenceTransformer
            return SentenceTransformer(settings.embedding_model)
    except Exception as e:
        logger.error(f"Error initializing embedding model: {e}")
        raise
