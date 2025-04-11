# Open WebUI Backend Microservices

This directory contains the backend microservices for Open WebUI.

## Architecture

The backend is structured into the following microservices:

- **API Gateway**: Entry point for all client requests
- **Inference Service**: Handles LLM model inference
- **Agent Service**: Orchestrates agents and multi-step workflows
- **Retrieval Service**: Performs vector/keyword search and document retrieval
- **Chat Service**: Manages chat sessions and message history

Additionally, there are shared components:

- **Common**: Shared utilities, helpers, and schemas
- **Deployments**: Docker Compose & Kubernetes configurations
- **CI-CD**: CI/CD pipelines and helper scripts
- **Docs**: Architecture and API documentation

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for deployment)
- PostgreSQL (for production)

### Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies for each service:

```bash
cd api-gateway
pip install -r requirements.txt
cd ../inference-service
pip install -r requirements.txt
# Repeat for other services
```

3. Run services individually for development:

```bash
cd api-gateway
uvicorn app.main:app --reload --port 8000
```

### Deployment

For deployment using Docker Compose:

```bash
cd deployments
cp .env.example .env
# Edit .env file with your configuration
docker-compose up -d
```

See the [Deployments README](deployments/README.md) for more details.

## Service Structure

Each microservice follows a standard structure:

```
app/
├── main.py                # FastAPI app initialization & router inclusion
├── models/                # Pydantic data models
├── routes/                # FastAPI route definitions
├── services/              # Business logic
└── core/config.py         # Service-specific configuration

tests/
├── test_<service>.py      # Unit or integration tests

requirements.txt
Dockerfile
README.md
```

## API Documentation

When running each service, API documentation is available at:

- API Gateway: http://localhost:8000/docs
- Inference Service: http://localhost:8001/docs
- Agent Service: http://localhost:8002/docs
- Retrieval Service: http://localhost:8003/docs
- Chat Service: http://localhost:8004/docs

## Testing

To run tests for a service:

```bash
cd <service-directory>
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
