import logging
import httpx
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.models.tools import Tool, ToolSpec

logger = logging.getLogger(__name__)

# Built-in tools
BUILT_IN_TOOLS = [
    Tool(
        name="web_search",
        description="Search the web for information",
        spec=ToolSpec(
            name="web_search",
            description="Search the web for information",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                    "engine": {
                        "type": "string",
                        "description": "The search engine to use",
                        "enum": ["google", "bing", "duckduckgo"],
                        "default": "duckduckgo",
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "The number of results to return",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
            returns={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "snippet": {"type": "string"},
                            },
                        },
                    },
                },
            },
        ),
    ),
    Tool(
        name="calculator",
        description="Perform mathematical calculations",
        spec=ToolSpec(
            name="calculator",
            description="Perform mathematical calculations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate",
                    },
                },
                "required": ["expression"],
            },
            returns={
                "type": "object",
                "properties": {
                    "result": {"type": "number"},
                },
            },
        ),
    ),
]


async def list_tools() -> List[Tool]:
    """
    List all available tools
    """
    try:
        tools = BUILT_IN_TOOLS.copy()
        
        # Add tools from tool servers
        for server_name, server_config in settings.tool_server_connections.items():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{server_config['url']}/tools",
                        headers={
                            "Authorization": f"Bearer {server_config.get('key', '')}",
                        },
                        timeout=5.0,
                    )
                    response.raise_for_status()
                    
                    server_tools = response.json()
                    for tool in server_tools:
                        tools.append(
                            Tool(
                                name=tool["name"],
                                description=tool["description"],
                                spec=ToolSpec(**tool["spec"]),
                                server={
                                    "name": server_name,
                                    "url": server_config["url"],
                                },
                            )
                        )
            except Exception as e:
                logger.error(f"Error fetching tools from {server_name}: {e}")
        
        return tools
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise


async def execute_tool(
    tool_name: str,
    params: Dict[str, Any],
    user_id: str,
) -> Any:
    """
    Execute a tool
    """
    try:
        # Get all tools
        tools = await list_tools()
        
        # Find the tool
        tool = next((t for t in tools if t.name == tool_name), None)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        # Execute the tool
        if tool.server:
            # External tool
            return await execute_external_tool(tool, params, user_id)
        else:
            # Built-in tool
            return await execute_built_in_tool(tool, params)
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        raise


async def execute_built_in_tool(tool: Tool, params: Dict[str, Any]) -> Any:
    """
    Execute a built-in tool
    """
    try:
        if tool.name == "web_search":
            return await execute_web_search(params)
        elif tool.name == "calculator":
            return await execute_calculator(params)
        else:
            raise ValueError(f"Unknown built-in tool: {tool.name}")
    except Exception as e:
        logger.error(f"Error executing built-in tool: {e}")
        raise


async def execute_external_tool(tool: Tool, params: Dict[str, Any], user_id: str) -> Any:
    """
    Execute an external tool
    """
    try:
        server_config = settings.tool_server_connections.get(tool.server["name"])
        if not server_config:
            raise ValueError(f"Tool server not found: {tool.server['name']}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{server_config['url']}/tools/{tool.name}/execute",
                headers={
                    "Authorization": f"Bearer {server_config.get('key', '')}",
                    "X-User-ID": user_id,
                },
                json=params,
                timeout=30.0,
            )
            response.raise_for_status()
            
            return response.json()
    except Exception as e:
        logger.error(f"Error executing external tool: {e}")
        raise


# Built-in tool implementations
async def execute_web_search(params: Dict[str, Any]) -> Any:
    """
    Execute a web search
    """
    # This is a placeholder implementation
    # In a real implementation, this would call the retrieval service
    return {
        "results": [
            {
                "title": "Example Search Result",
                "url": "https://example.com",
                "snippet": "This is an example search result.",
            }
        ]
    }


async def execute_calculator(params: Dict[str, Any]) -> Any:
    """
    Execute a calculator
    """
    try:
        expression = params["expression"]
        # Use eval with a restricted environment for safety
        # This is just a simple example - in a real implementation,
        # you would use a safer approach like a math expression parser
        result = eval(expression, {"__builtins__": {}}, {"abs": abs, "max": max, "min": min, "sum": sum})
        return {"result": result}
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")
