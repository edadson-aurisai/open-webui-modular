import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.core.config import settings
from app.models.pipelines import PipelineResponse, PipelineListItem, PipelineStep
from app.services.tools import execute_tool

logger = logging.getLogger(__name__)

# In-memory database of pipelines (would be replaced with a real database in production)
pipelines_db = {}


async def create_pipeline(
    user_id: str,
    name: str,
    description: Optional[str] = None,
    steps: List[PipelineStep] = [],
) -> str:
    """
    Create a new pipeline
    """
    try:
        # Generate a pipeline ID
        pipeline_id = str(uuid.uuid4())
        
        # Create the pipeline
        now = datetime.now()
        pipelines_db[pipeline_id] = {
            "id": pipeline_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "steps": steps,
            "created_at": now,
            "updated_at": now,
        }
        
        return pipeline_id
    except Exception as e:
        logger.error(f"Error creating pipeline: {e}")
        raise


async def update_pipeline(
    pipeline_id: str,
    user_id: str,
    name: str,
    description: Optional[str] = None,
    steps: List[PipelineStep] = [],
) -> Optional[PipelineResponse]:
    """
    Update a pipeline
    """
    try:
        # Check if the pipeline exists and belongs to the user
        if pipeline_id not in pipelines_db or pipelines_db[pipeline_id]["user_id"] != user_id:
            return None
        
        # Update the pipeline
        pipelines_db[pipeline_id].update({
            "name": name,
            "description": description,
            "steps": steps,
            "updated_at": datetime.now(),
        })
        
        return PipelineResponse(**pipelines_db[pipeline_id])
    except Exception as e:
        logger.error(f"Error updating pipeline: {e}")
        raise


async def get_pipeline(
    pipeline_id: str,
    user_id: str,
) -> Optional[PipelineResponse]:
    """
    Get a pipeline by ID
    """
    try:
        # Check if the pipeline exists and belongs to the user
        if pipeline_id not in pipelines_db or pipelines_db[pipeline_id]["user_id"] != user_id:
            return None
        
        return PipelineResponse(**pipelines_db[pipeline_id])
    except Exception as e:
        logger.error(f"Error getting pipeline: {e}")
        raise


async def list_pipelines(
    user_id: str,
) -> List[PipelineListItem]:
    """
    List all pipelines for a user
    """
    try:
        # Filter pipelines by user ID
        user_pipelines = [
            PipelineListItem(
                id=pipeline_id,
                name=pipeline["name"],
                description=pipeline["description"],
                created_at=pipeline["created_at"],
                updated_at=pipeline["updated_at"],
            )
            for pipeline_id, pipeline in pipelines_db.items()
            if pipeline["user_id"] == user_id
        ]
        
        # Sort by name
        user_pipelines.sort(key=lambda x: x.name)
        
        return user_pipelines
    except Exception as e:
        logger.error(f"Error listing pipelines: {e}")
        raise


async def delete_pipeline(
    pipeline_id: str,
    user_id: str,
) -> bool:
    """
    Delete a pipeline
    """
    try:
        # Check if the pipeline exists and belongs to the user
        if pipeline_id not in pipelines_db or pipelines_db[pipeline_id]["user_id"] != user_id:
            return False
        
        # Delete the pipeline
        del pipelines_db[pipeline_id]
        
        return True
    except Exception as e:
        logger.error(f"Error deleting pipeline: {e}")
        raise


async def execute_pipeline(
    pipeline_id: str,
    user_id: str,
    inputs: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Execute a pipeline
    """
    try:
        # Get the pipeline
        pipeline = await get_pipeline(pipeline_id, user_id)
        if not pipeline:
            raise ValueError(f"Pipeline not found: {pipeline_id}")
        
        # Initialize the pipeline state
        state = {
            "inputs": inputs,
            "outputs": {},
        }
        
        # Execute each step in order
        for step in pipeline.steps:
            # Get the step inputs from the pipeline state
            step_inputs = {}
            for input_name, input_path in step.inputs.items():
                # Parse the input path (e.g., "inputs.query" or "steps.step1.output")
                parts = input_path.split(".")
                if parts[0] == "inputs":
                    if len(parts) > 1 and parts[1] in inputs:
                        step_inputs[input_name] = inputs[parts[1]]
                elif parts[0] == "steps" and len(parts) > 2:
                    step_id = parts[1]
                    if step_id in state["outputs"] and parts[2] in state["outputs"][step_id]:
                        step_inputs[input_name] = state["outputs"][step_id][parts[2]]
            
            # Execute the step
            if step.type == "tool":
                # Execute a tool
                tool_name = step.config.get("tool_name")
                if not tool_name:
                    raise ValueError(f"Tool name not specified for step: {step.id}")
                
                step_result = await execute_tool(tool_name, step_inputs, user_id)
            elif step.type == "transform":
                # Apply a transformation
                transform_type = step.config.get("transform_type")
                if not transform_type:
                    raise ValueError(f"Transform type not specified for step: {step.id}")
                
                step_result = await execute_transform(transform_type, step_inputs)
            else:
                raise ValueError(f"Unknown step type: {step.type}")
            
            # Store the step outputs in the pipeline state
            state["outputs"][step.id] = step_result
        
        # Collect the pipeline outputs
        outputs = {}
        for step in pipeline.steps:
            for output_name, output_path in step.outputs.items():
                if output_path.startswith("outputs."):
                    output_key = output_path.split(".")[1]
                    if step.id in state["outputs"]:
                        outputs[output_key] = state["outputs"][step.id].get(output_name)
        
        return outputs
    except Exception as e:
        logger.error(f"Error executing pipeline: {e}")
        raise


async def execute_transform(transform_type: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a transformation
    """
    try:
        if transform_type == "join":
            # Join multiple strings
            separator = inputs.get("separator", " ")
            strings = inputs.get("strings", [])
            result = separator.join(strings)
            return {"result": result}
        elif transform_type == "filter":
            # Filter a list
            items = inputs.get("items", [])
            condition = inputs.get("condition", {})
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            
            if not field or not operator:
                return {"result": items}
            
            filtered_items = []
            for item in items:
                if field in item:
                    if operator == "eq" and item[field] == value:
                        filtered_items.append(item)
                    elif operator == "neq" and item[field] != value:
                        filtered_items.append(item)
                    elif operator == "gt" and item[field] > value:
                        filtered_items.append(item)
                    elif operator == "gte" and item[field] >= value:
                        filtered_items.append(item)
                    elif operator == "lt" and item[field] < value:
                        filtered_items.append(item)
                    elif operator == "lte" and item[field] <= value:
                        filtered_items.append(item)
                    elif operator == "contains" and value in item[field]:
                        filtered_items.append(item)
            
            return {"result": filtered_items}
        else:
            raise ValueError(f"Unknown transform type: {transform_type}")
    except Exception as e:
        logger.error(f"Error executing transform: {e}")
        raise
