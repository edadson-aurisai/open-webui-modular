import logging
import httpx
from typing import Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)


async def execute_code(
    code: str,
    language: str = "python",
    user_id: str = None,
) -> str:
    """
    Execute code
    """
    try:
        if not settings.enable_code_execution:
            raise ValueError("Code execution is disabled")
        
        if settings.code_execution_engine == "jupyter":
            return await execute_code_jupyter(code, language)
        else:
            raise ValueError(f"Unknown code execution engine: {settings.code_execution_engine}")
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        raise


async def run_code_interpreter(
    query: str,
    context: str = None,
    user_id: str = None,
) -> str:
    """
    Run code interpreter
    """
    try:
        if not settings.enable_code_interpreter:
            raise ValueError("Code interpreter is disabled")
        
        if settings.code_interpreter_engine == "jupyter":
            return await run_code_interpreter_jupyter(query, context)
        else:
            raise ValueError(f"Unknown code interpreter engine: {settings.code_interpreter_engine}")
    except Exception as e:
        logger.error(f"Error running code interpreter: {e}")
        raise


async def execute_code_jupyter(code: str, language: str) -> str:
    """
    Execute code using Jupyter
    """
    try:
        # Prepare the request payload
        payload = {
            "code": code,
            "language": language,
        }
        
        # Send the request to the Jupyter server
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.code_execution_jupyter_url}/api/execute",
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("output", "")
    except Exception as e:
        logger.error(f"Error executing code with Jupyter: {e}")
        raise


async def run_code_interpreter_jupyter(query: str, context: str = None) -> str:
    """
    Run code interpreter using Jupyter
    """
    try:
        # Prepare the request payload
        payload = {
            "query": query,
        }
        
        if context:
            payload["context"] = context
        
        # Send the request to the Jupyter server
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.code_interpreter_jupyter_url}/api/interpret",
                json=payload,
                timeout=60.0,
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("output", "")
    except Exception as e:
        logger.error(f"Error running code interpreter with Jupyter: {e}")
        raise
