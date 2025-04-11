# Open WebUI Microservices Deployment

This directory contains deployment configurations for the Open WebUI microservices architecture.

## Docker Compose

The `docker-compose.yml` file provides a complete deployment setup for all microservices:

- API Gateway
- Inference Service
- Agent Service
- Retrieval Service
- Chat Service
- PostgreSQL Database
- Ollama (for local LLM inference)

### Getting Started

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file to configure your deployment.

3. Start the services:

```bash
docker-compose up -d
```

4. Access the API Gateway at http://localhost:8000

### Configuration

Each service can be configured through environment variables. See the `.env.example` file for available options.

### Volumes

The deployment uses the following volumes:

- `postgres-data`: PostgreSQL database data
- `retrieval-data`: Uploaded files for retrieval
- `chroma-data`: Vector database for embeddings
- `ollama-data`: Ollama model files

## Kubernetes

For Kubernetes deployment, use the manifests in the `kubernetes` directory.

```bash
kubectl apply -f kubernetes/
```

## Production Deployment

For production deployments, consider the following:

1. Use a proper secrets management solution
2. Configure TLS for all services
3. Set up proper monitoring and logging
4. Use a managed database service instead of the containerized PostgreSQL
5. Configure resource limits for all containers
