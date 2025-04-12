# Testing Backend Services with Uvicorn

This guide explains how to test the Open WebUI backend microservices using Uvicorn directly, without Docker or other containerization.

## Prerequisites

- Python 3.11+ installed
- PostgreSQL (optional, for chat-service with persistent storage)

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install base dependencies:

```bash
pip install uvicorn fastapi
```

## Testing Individual Services

Use the `test-service.sh` script to test a specific service:

```bash
./test-service.sh <service-name>
```

Available services:
- `api-gateway` (port 8000)
- `inference-service` (port 8001)
- `agent-service` (port 8002)
- `retrieval-service` (port 8003)
- `chat-service` (port 8004)

Example:
```bash
./test-service.sh inference-service
```

This will:
1. Install the required dependencies for the service
2. Load environment variables from `backend/.env.dev`
3. Start the service using Uvicorn on the appropriate port

## Running All Services

To run all services simultaneously:

```bash
./run-all-services.sh
```

This will start all five microservices in the background, each on its own port.

## Accessing Services

Once running, you can access the services at:

- API Gateway: http://localhost:8000
- Inference Service: http://localhost:8001
- Agent Service: http://localhost:8002
- Retrieval Service: http://localhost:8003
- Chat Service: http://localhost:8004

Each service provides a root endpoint (`/`) with information about available endpoints, and a Swagger UI documentation page at `/docs`.

## Environment Configuration

The services use environment variables from `backend/.env.dev`. You can modify this file to change configuration options.

Key configuration options:
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `DATABASE_URL`: PostgreSQL connection string (for chat-service)
- `OLLAMA_BASE_URLS`: URL for Ollama API (for inference-service)
- `OPENAI_API_KEYS`: OpenAI API keys (for inference-service)

## Troubleshooting

If you encounter issues:

1. Check that the required dependencies are installed:
   ```bash
   pip install -r backend/<service-name>/requirements.txt
   ```

2. Verify that the service port is not already in use:
   ```bash
   lsof -i :<port>
   ```

3. Check the logs for error messages.

4. Ensure PostgreSQL is running if testing the chat-service with database functionality.
