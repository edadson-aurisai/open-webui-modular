from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile, File, Form
from typing import List, Dict, Any, Optional
import os
import uuid
import shutil

from app.core.config import settings
from app.models.files import (
    FileUploadResponse,
    FileListResponse,
    FileDeleteResponse,
)
from app.services.files import (
    process_file,
    list_files,
    delete_file,
)

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    collection_name: str = Form(...),
):
    """
    Upload a file and process it for retrieval
    """
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Generate a unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(settings.upload_dir, filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the file
        document_ids = await process_file(
            file_path=file_path,
            original_filename=file.filename,
            collection_name=collection_name,
        )
        
        return FileUploadResponse(
            id=file_id,
            filename=file.filename,
            document_ids=document_ids,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}",
        )

@router.get("/list", response_model=FileListResponse)
async def list_files_endpoint(request: Request, collection_name: Optional[str] = None):
    """
    List all files
    """
    try:
        files = await list_files(collection_name)
        return FileListResponse(
            files=files,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing files: {str(e)}",
        )

@router.delete("/{file_id}", response_model=FileDeleteResponse)
async def delete_file_endpoint(request: Request, file_id: str):
    """
    Delete a file
    """
    try:
        success = await delete_file(file_id)
        return FileDeleteResponse(
            success=success,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting file: {str(e)}",
        )
