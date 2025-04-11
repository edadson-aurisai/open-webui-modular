import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.knowledge import KnowledgeBase, KnowledgeBaseQueryResult
from app.services.vector import search_vectors

logger = logging.getLogger(__name__)

# In-memory database of knowledge bases (would be replaced with a real database in production)
kb_db = {}


async def create_knowledge_base(
    name: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a new knowledge base
    """
    try:
        # Generate a knowledge base ID
        kb_id = str(uuid.uuid4())
        
        # Store knowledge base information
        kb_db[kb_id] = {
            "id": kb_id,
            "name": name,
            "description": description,
            "document_count": 0,
            "created_at": datetime.now(),
            "metadata": metadata or {},
        }
        
        return kb_id
    except Exception as e:
        logger.error(f"Error creating knowledge base: {e}")
        raise


async def list_knowledge_bases() -> List[KnowledgeBase]:
    """
    List all knowledge bases
    """
    try:
        kb_list = [KnowledgeBase(**kb_info) for kb_id, kb_info in kb_db.items()]
        return kb_list
    except Exception as e:
        logger.error(f"Error listing knowledge bases: {e}")
        raise


async def delete_knowledge_base(kb_id: str) -> bool:
    """
    Delete a knowledge base
    """
    try:
        if kb_id not in kb_db:
            return False
        
        # Delete the knowledge base
        del kb_db[kb_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting knowledge base: {e}")
        raise


async def query_knowledge_base(
    kb_id: str,
    query: str,
    k: int = 5,
    filter: Optional[Dict[str, Any]] = None,
) -> List[KnowledgeBaseQueryResult]:
    """
    Query a knowledge base
    """
    try:
        if kb_id not in kb_db:
            raise ValueError(f"Knowledge base {kb_id} not found")
        
        # Get knowledge base information
        kb_info = kb_db[kb_id]
        
        # Add knowledge base filter
        if filter is None:
            filter = {}
        filter["kb_id"] = kb_id
        
        # Search the vector database
        results = await search_vectors(
            collection_name="knowledge_bases",
            query=query,
            k=k,
            filter=filter,
        )
        
        # Convert to KnowledgeBaseQueryResult objects
        query_results = [
            KnowledgeBaseQueryResult(
                id=result.id,
                text=result.text,
                metadata=result.metadata,
                score=result.score,
            )
            for result in results
        ]
        
        return query_results
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        raise
