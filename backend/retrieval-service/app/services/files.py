import logging
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import mimetypes

from app.core.config import settings
from app.models.files import FileInfo
from app.services.vector import upsert_vectors
from app.services.document_loaders import load_document

logger = logging.getLogger(__name__)

# In-memory database of files (would be replaced with a real database in production)
files_db = {}


async def process_file(
    file_path: str,
    original_filename: str,
    collection_name: str,
) -> List[str]:
    """
    Process a file for retrieval
    """
    try:
        # Generate a file ID
        file_id = str(uuid.uuid4())
        
        # Determine the file type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Load the document
        documents = await load_document(file_path, mime_type)
        
        # Upsert the documents into the vector database
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Add file_id to metadata
        for metadata in metadatas:
            metadata["file_id"] = file_id
        
        document_ids = await upsert_vectors(
            collection_name=collection_name,
            texts=texts,
            metadatas=metadatas,
        )
        
        # Store file information
        files_db[file_id] = {
            "id": file_id,
            "filename": original_filename,
            "collection_name": collection_name,
            "document_count": len(documents),
            "created_at": datetime.now(),
            "document_ids": document_ids,
            "metadata": {
                "mime_type": mime_type,
                "file_path": file_path,
            },
        }
        
        return document_ids
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise


async def list_files(collection_name: Optional[str] = None) -> List[FileInfo]:
    """
    List all files
    """
    try:
        if collection_name:
            # Filter by collection name
            file_list = [
                FileInfo(**file_info)
                for file_id, file_info in files_db.items()
                if file_info["collection_name"] == collection_name
            ]
        else:
            # Return all files
            file_list = [FileInfo(**file_info) for file_id, file_info in files_db.items()]
        
        return file_list
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise


async def delete_file(file_id: str) -> bool:
    """
    Delete a file
    """
    try:
        if file_id not in files_db:
            return False
        
        # Get file information
        file_info = files_db[file_id]
        
        # Delete the file from disk
        if os.path.exists(file_info["metadata"]["file_path"]):
            os.remove(file_info["metadata"]["file_path"])
        
        # Delete the documents from the vector database
        # This would be implemented in a real system
        
        # Remove from the in-memory database
        del files_db[file_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise
