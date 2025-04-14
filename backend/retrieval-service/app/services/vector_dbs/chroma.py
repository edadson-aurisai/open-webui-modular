import logging
from typing import List, Dict, Any, Optional
import chromadb

from app.core.config import settings
from app.models.vector import VectorSearchResult

logger = logging.getLogger(__name__)


class ChromaClient:
    """
    Client for Chroma vector database
    """

    def __init__(self):
        """
        Initialize the Chroma client
        """
        try:
            # Initialize the client with the new API
            self.client = chromadb.PersistentClient(
                path="./chroma_db"
            )
            logger.info("Initialized Chroma client")
        except Exception as e:
            logger.error(f"Error initializing Chroma client: {e}")
            raise

    async def search(
        self,
        collection_name: str,
        query_embedding: List[float],
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Search for vectors in the collection
        """
        try:
            # Get or create the collection
            collection = self.client.get_or_create_collection(collection_name)

            # Search the collection
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter,
                include=["documents", "metadatas", "distances"],
            )

            return results
        except Exception as e:
            logger.error(f"Error searching Chroma collection: {e}")
            raise

    async def upsert(
        self,
        collection_name: str,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Upsert vectors into the collection
        """
        try:
            # Get or create the collection
            collection = self.client.get_or_create_collection(collection_name)

            # Upsert the vectors
            collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )
        except Exception as e:
            logger.error(f"Error upserting to Chroma collection: {e}")
            raise

    async def delete(
        self,
        collection_name: str,
        ids: Optional[List[str]] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Delete vectors from the collection
        """
        try:
            # Get the collection
            try:
                collection = self.client.get_collection(collection_name)
            except ValueError:
                # Collection doesn't exist
                return

            # Delete the vectors
            if ids:
                collection.delete(ids=ids)
            elif filter:
                collection.delete(where=filter)
        except Exception as e:
            logger.error(f"Error deleting from Chroma collection: {e}")
            raise
