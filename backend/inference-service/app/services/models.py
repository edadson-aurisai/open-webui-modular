import logging
import aiohttp
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.models import ModelResponse, ModelParams, ModelMeta

logger = logging.getLogger(__name__)


async def get_all_models() -> List[ModelResponse]:
    """
    Get all available models from Ollama and OpenAI
    """
    models = []
    
    # Get Ollama models
    if settings.enable_ollama_api:
        for i, url in enumerate(settings.ollama_base_urls):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{url}/api/tags") as response:
                        if response.status == 200:
                            data = await response.json()
                            for model in data.get("models", []):
                                model_id = model.get("name", "")
                                
                                # Apply prefix if configured
                                api_config = settings.ollama_api_configs.get(
                                    str(i),
                                    settings.ollama_api_configs.get(url, {}),
                                )
                                prefix_id = api_config.get("prefix_id", None)
                                if prefix_id:
                                    model_id = f"{prefix_id}.{model_id}"
                                
                                models.append(
                                    ModelResponse(
                                        id=model_id,
                                        name=model.get("name", ""),
                                        owned_by="ollama",
                                        params=ModelParams(
                                            model_format=model.get("details", {}).get("format"),
                                            model_family=model.get("details", {}).get("family"),
                                            model_families=model.get("details", {}).get("families"),
                                            parameter_size=model.get("details", {}).get("parameter_size"),
                                            quantization_level=model.get("details", {}).get("quantization_level"),
                                        ),
                                        meta=ModelMeta(
                                            description=model.get("description", ""),
                                            tags=["ollama"],
                                        ),
                                        created_at=None,
                                        updated_at=None,
                                    )
                                )
            except Exception as e:
                logger.error(f"Error fetching Ollama models from {url}: {e}")
    
    # Get OpenAI models
    if settings.enable_openai_api:
        for i, url in enumerate(settings.openai_api_base_urls):
            if i < len(settings.openai_api_keys):
                try:
                    async with aiohttp.ClientSession() as session:
                        headers = {"Authorization": f"Bearer {settings.openai_api_keys[i]}"}
                        async with session.get(f"{url}/models", headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                for model in data.get("data", []):
                                    models.append(
                                        ModelResponse(
                                            id=model.get("id", ""),
                                            name=model.get("id", ""),
                                            owned_by="openai",
                                            params=None,
                                            meta=ModelMeta(
                                                tags=["openai"],
                                            ),
                                            created_at=None,
                                            updated_at=None,
                                        )
                                    )
                except Exception as e:
                    logger.error(f"Error fetching OpenAI models from {url}: {e}")
    
    return models


async def get_all_base_models() -> List[ModelResponse]:
    """
    Get all available base models
    """
    # For now, just return all models
    # In a real implementation, this would filter for base models only
    return await get_all_models()
