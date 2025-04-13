# Inference Service

The Inference Service handles LLM model inference for Open WebUI.

## Features

- Ollama integration
- OpenAI integration
- Model management
- Inference optimization
- Streaming responses

## API Endpoints

- `/api/v1/ollama` - Ollama API endpoints
- `/api/v1/openai` - OpenAI API endpoints
- `/api/v1/models` - Model management endpoints

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
    uvicorn app.main:app --reload --port 8003
    ```

### Environment Variables

- `ENABLE_OLLAMA_API` - Enable Ollama API
- `OLLAMA_BASE_URLS` - Ollama base URLs
- `OLLAMA_API_CONFIGS` - Ollama API configurations
- `ENABLE_OPENAI_API` - Enable OpenAI API
- `OPENAI_API_BASE_URLS` - OpenAI API base URLs
- `OPENAI_API_KEYS` - OpenAI API keys
- `ENABLE_DIRECT_CONNECTIONS` - Enable direct connections
- `JWT_SECRET_KEY` - JWT secret key

## Testing

Run tests with:
    ```bash
    pytest
    ```

## Deployment

See the [Deployments README](../deployments/README.md) for deployment instructions.
