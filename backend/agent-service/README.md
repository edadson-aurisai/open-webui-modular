# Agent Service

The Agent Service orchestrates agents and multi-step workflows for Open WebUI.

## Features

- Task management
- Function calling
- Tool integration
- Pipeline processing
- Workflow orchestration
- Code execution
- Code interpreter

## API Endpoints

- `/api/v1/tasks` - Task management
- `/api/v1/tools` - Tool management
- `/api/v1/pipelines` - Pipeline management
- `/api/v1/code` - Code execution and interpretation

## Development

### Prerequisites

- Python 3.11+

### Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the service:

```bash
uvicorn app.main:app --reload --port 8002
```

### Environment Variables

- `ENABLE_CODE_EXECUTION` - Enable code execution
- `CODE_EXECUTION_ENGINE` - Code execution engine
- `CODE_EXECUTION_JUPYTER_URL` - Jupyter URL for code execution
- `ENABLE_CODE_INTERPRETER` - Enable code interpreter
- `CODE_INTERPRETER_ENGINE` - Code interpreter engine
- `CODE_INTERPRETER_JUPYTER_URL` - Jupyter URL for code interpreter
- `ENABLE_TOOLS` - Enable tools
- `TOOL_SERVER_CONNECTIONS` - Tool server connections
- `TASK_MODEL` - Task model
- `TASK_MODEL_EXTERNAL` - Use external task model
- `INFERENCE_SERVICE_URL` - Inference service URL
- `JWT_SECRET_KEY` - JWT secret key

## Testing

Run tests with:

```bash
pytest
```

## Deployment

See the [Deployments README](../deployments/README.md) for deployment instructions.
