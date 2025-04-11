import logging
from typing import List, Dict, Any, Optional
import uuid

from app.core.config import settings
from app.models.vector import VectorSearchResult

# Import the appropriate vector database client based on configuration
if settings.vector_db == "chroma":
    from app.services.vector_dbs.chroma import ChromaClient as VectorDBClient
elif settings.vector_db == "milvus":
    from app.services.vector_dbs.milvus import MilvusClient as VectorDBClient
elif settings.vector_db == "qdrant":
    from app.services.vector_dbs.qdrant import QdrantClient as VectorDBClient
elif settings.vector_db == "opensearch":
    from app.services.vector_dbs.opensearch import OpenSearchClient as VectorDBClient
elif settings.vector_db == "pgvector":
    from app.services.vector_dbs.pgvector import PgvectorClient as VectorDBClient
elif settings.vector_db == "elasticsearch":
    from app.services.vector_dbs.elasticsearch import ElasticsearchClient as VectorDBClient
else:
    # Default to Chroma
    from app.services.vector_dbs.chroma import ChromaClient as VectorDBClient

# Initialize the vector database client
vector_db_client = VectorDBClient()

# Initialize the embedding model
from app.services.embeddings import get_embedding_model
embedding_model = get_embedding_model()

logger = logging.getLogger(__name__)


async def search_vectors(
    collection_name: str,
    query: str,
    k: int = 5,
    filter: Optional[Dict[str, Any]] = None,
) -> List[VectorSearchResult]:
    """
    Search for vectors in the vector database
    """
    try:
        # Get the embedding for the query
        query_embedding = await get_embedding(query)
        
        # Search the vector database
        results = await vector_db_client.search(
            collection_name=collection_name,
            query_embedding=query_embedding,
            k=k,
            filter=filter,
        )
        
        # Convert to VectorSearchResult objects
        search_results = []
        for i in range(len(results.ids[0])):
            search_results.append(
                VectorSearchResult(
                    id=results.ids[0][i],
                    text=results.documents[0][i],
                    metadata=results.metadatas[0][i],
                    score=results.distances[0][i],
                )
            )
        
        return search_results
    except Exception as e:
        logger.error(f"Error searching vectors: {e}")
        raise


async def upsert_vectors(
    collection_name: str,
    texts: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
) -> List[str]:
    """
    Upsert vectors into the vector database
    """
    try:
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(texts))]
        
        # Generate embeddings for the texts
        embeddings = []
        for text in texts:
            embedding = await get_embedding(text)
            embeddings.append(embedding)
        
        # Upsert into the vector database
        await vector_db_client.upsert(
            collection_name=collection_name,
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        
        return ids
    except Exception as e:
        logger.error(f"Error upserting vectors: {e}")
        raise


async def delete_vectors(
    collection_name: str,
    ids: Optional[List[str]] = None,
    filter: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Delete vectors from the vector database
    """
    try:
        # Delete from the vector database
        await vector_db_client.delete(
            collection_name=collection_name,
            ids=ids,
            filter=filter,
        )
        
        return True
    except Exception as e:
        logger.error(f"Error deleting vectors: {e}")
        raise


async def get_embedding(text: str) -> List[float]:
    """
    Get embedding for a text
    """
    try:
        # Get the embedding
        embedding = embedding_model.encode(text).tolist()
        return embedding
    except Exception as e:
        logger.error(f"Error getting embedding: {e}")
        raise
