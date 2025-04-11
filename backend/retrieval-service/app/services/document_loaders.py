import logging
from typing import List, Dict, Any, Optional
import os

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


async def load_document(file_path: str, mime_type: Optional[str] = None) -> List[Document]:
    """
    Load a document from a file
    """
    try:
        # Determine the file type if not provided
        if mime_type is None:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
        else:
            ext = mime_type
        
        # Load the document based on file type
        if ext in [".txt", "text/plain"]:
            return await load_text(file_path)
        elif ext in [".pdf", "application/pdf"]:
            return await load_pdf(file_path)
        elif ext in [".docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return await load_docx(file_path)
        elif ext in [".csv", "text/csv"]:
            return await load_csv(file_path)
        elif ext in [".md", "text/markdown"]:
            return await load_markdown(file_path)
        elif ext in [".html", ".htm", "text/html"]:
            return await load_html(file_path)
        else:
            # Default to text
            return await load_text(file_path)
    except Exception as e:
        logger.error(f"Error loading document: {e}")
        raise


async def load_text(file_path: str) -> List[Document]:
    """
    Load a text document
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        docs = text_splitter.create_documents([text])
        
        # Add metadata
        for doc in docs:
            doc.metadata["source"] = file_path
            doc.metadata["file_type"] = "text"
        
        return docs
    except Exception as e:
        logger.error(f"Error loading text document: {e}")
        raise


async def load_pdf(file_path: str) -> List[Document]:
    """
    Load a PDF document
    """
    try:
        from langchain_community.document_loaders import PyPDFLoader
        
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        docs = text_splitter.split_documents(docs)
        
        return docs
    except Exception as e:
        logger.error(f"Error loading PDF document: {e}")
        raise


async def load_docx(file_path: str) -> List[Document]:
    """
    Load a DOCX document
    """
    try:
        from langchain_community.document_loaders import Docx2txtLoader
        
        loader = Docx2txtLoader(file_path)
        docs = loader.load()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        docs = text_splitter.split_documents(docs)
        
        return docs
    except Exception as e:
        logger.error(f"Error loading DOCX document: {e}")
        raise


async def load_csv(file_path: str) -> List[Document]:
    """
    Load a CSV document
    """
    try:
        from langchain_community.document_loaders import CSVLoader
        
        loader = CSVLoader(file_path)
        docs = loader.load()
        
        return docs
    except Exception as e:
        logger.error(f"Error loading CSV document: {e}")
        raise


async def load_markdown(file_path: str) -> List[Document]:
    """
    Load a Markdown document
    """
    try:
        from langchain_community.document_loaders import UnstructuredMarkdownLoader
        
        loader = UnstructuredMarkdownLoader(file_path)
        docs = loader.load()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        docs = text_splitter.split_documents(docs)
        
        return docs
    except Exception as e:
        logger.error(f"Error loading Markdown document: {e}")
        raise


async def load_html(file_path: str) -> List[Document]:
    """
    Load an HTML document
    """
    try:
        from langchain_community.document_loaders import BSHTMLLoader
        
        loader = BSHTMLLoader(file_path)
        docs = loader.load()
        
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        
        docs = text_splitter.split_documents(docs)
        
        return docs
    except Exception as e:
        logger.error(f"Error loading HTML document: {e}")
        raise
