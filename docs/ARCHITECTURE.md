# Open WebUI Architecture

This document describes the microservices architecture of Open WebUI, detailing how the different components interact and their specific responsibilities.

## Overview

Open WebUI is built on a microservices architecture, with each service handling specific functionality. All client requests are routed through an API Gateway, which then forwards them to the appropriate service.

## System Architecture

```
                                    ┌─────────────────┐
                                    │                 │
                                    │  API Gateway    │
                                    │    (8000)       │
                                    │                 │
                                    └────────┬────────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
            ┌───────▼──────┐        ┌──────▼───────┐        ┌─────▼───────┐
            │              │        │              │        │             │
            │    Chat      │        │  Inference   │        │   Agent     │
            │   Service    │        │   Service    │        │  Service    │
            │    (8004)    │        │    (8001)    │        │   (8002)    │
            │              │        │              │        │             │
            └──────────────┘        └──────────────┘        └─────────────┘
                                           │
                                   ┌───────▼──────┐
                                   │              │
                                   │  Retrieval   │
                                   │   Service    │
                                   │    (8003)    │
                                   │              │
                                   └──────────────┘
```

## Service Responsibilities

### API Gateway (Port 8000)

The API Gateway serves as the entry point for all client requests and provides:
- Request routing to appropriate microservices
- Authentication and authorization
- Request validation
- Rate limiting
- CORS handling
- Session management

### Chat Service (Port 8004)

Manages chat-related functionality:
- Chat session management
- Message storage and retrieval
- Chat history
- User preferences
- Chat metadata (tags, folders)
- Chat sharing capabilities

### Inference Service (Port 8001)

Handles all LLM model interactions:
- Integration with multiple model providers:
  - Ollama
  - OpenAI-compatible APIs
- Model management
- Inference optimization
- Streaming responses
- Model configuration

### Agent Service (Port 8002)

Orchestrates AI agents and workflows:
- Task management
- Function calling
- Tool integration
- Pipeline processing
- Workflow orchestration
- Code execution
- Code interpreter

### Retrieval Service (Port 8003)

Manages search and document retrieval:
- Vector database integration
- Document processing
- Embedding generation
- Web search integration
- RAG (Retrieval Augmented Generation) implementation
- File management

## Communication

Services communicate via HTTP REST APIs. The API Gateway acts as a reverse proxy, routing requests to the appropriate service based on the URL path:

- `/api/v1/chats/*` → Chat Service
- `/api/v1/inference/*` → Inference Service
- `/api/v1/agents/*` → Agent Service
- `/api/v1/retrieval/*` → Retrieval Service

## Configuration

Services are configured through environment variables. Key configuration options include:

```env
# API Gateway
INFERENCE_SERVICE_URL=http://inference-service:8001
AGENT_SERVICE_URL=http://agent-service:8002
RETRIEVAL_SERVICE_URL=http://retrieval-service:8003
CHAT_SERVICE_URL=http://chat-service:8004
JWT_SECRET_KEY=your-secret-key

# Inference Service
ENABLE_OLLAMA_API=true
OLLAMA_BASE_URLS=http://ollama:11434
ENABLE_OPENAI_API=true
OPENAI_API_BASE_URLS=https://api.openai.com/v1

# Retrieval Service
VECTOR_DB=chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2
ENABLE_RAG_HYBRID_SEARCH=true
```

## Deployment

The services can be deployed using Docker Compose or Kubernetes:

### Docker Compose
```bash
cd backend/deployments
docker-compose up -d
```

### Kubernetes
```bash
kubectl apply -f kubernetes/
```

## Development

For local development, services can be run individually using Uvicorn:

```bash
# Example for running the inference service
cd backend/inference-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Security

- All API endpoints require JWT authentication except for public endpoints
- Services communicate over HTTP/HTTPS
- Environment variables are used for sensitive configuration
- Rate limiting is implemented at the API Gateway level
- CORS policies are enforced

## Data Storage

- Chat Service: PostgreSQL for chat and message storage
- Retrieval Service: Vector database (Chroma/Milvus/Qdrant) for embeddings
- File storage: Local filesystem or object storage for uploaded files