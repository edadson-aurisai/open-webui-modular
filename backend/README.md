# Open WebUI Backend

[![GitHub license](https://img.shields.io/badge/license-BSD--3--Clause-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-009688.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Supported-326CE5.svg)](https://kubernetes.io/)

**Open WebUI Backend** is a modular, extensible, and feature-rich AI platform backend designed to operate with various LLM providers. It supports Ollama, OpenAI-compatible APIs, and includes a built-in inference engine for RAG (Retrieval Augmented Generation), making it a powerful AI deployment solution.

![Open WebUI Architecture](docs/images/architecture.png)

*Note: You may need to create this architecture diagram in the docs/images directory.*

## Key Features ⭐

- 🚀 **Microservices Architecture**: Modular design with specialized services for inference, chat, retrieval, and agent orchestration

- 🔌 **Multiple LLM Provider Support**: Seamless integration with Ollama and OpenAI-compatible APIs (LMStudio, GroqCloud, Mistral, OpenRouter, etc.)

- 🔍 **Built-in RAG Engine**: Powerful retrieval augmented generation with vector database integration

- 🛠️ **Agent Framework**: Orchestrate complex AI workflows with function calling and tool integration

- 🔐 **Role-Based Access Control**: Granular permissions and user management

- 🌐 **Web Search Integration**: Connect to various search providers for enhanced RAG capabilities

- 📚 **Document Processing**: Process and index various document formats for knowledge retrieval

- 🧩 **Extensible Plugin System**: Easily extend functionality with custom plugins

- 🔄 **Streaming Responses**: Real-time streaming for chat completions

- 📊 **Observability**: Comprehensive logging and monitoring

## Microservices Overview

The backend consists of the following microservices:

### API Gateway (Port 8000)

Entry point for all client requests, handling routing, authentication, and request validation.

### Chat Service (Port 8001)

Manages chat sessions, message history, and conversation context.

### Agent Service (Port 8002)

Orchestrates AI agents, tools, and workflows for complex tasks.

### Inference Service (Port 8003)

Manages LLM interactions with multiple model providers (Ollama, OpenAI, etc.).

### Retrieval Service (Port 8004)

Handles vector search, document processing, and RAG functionality.

## Getting Started 🚀

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for production deployment)

### Quick Start with Docker Compose

1. Clone the repository:

   ```bash
   git clone https://github.com/your-org/open-webui-modular.git
   cd open-webui-modular/backend/deployments
   ```

2. Configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the services:

   ```bash
   docker-compose up -d
   ```

4. Access the API Gateway at <http://localhost:8000>

### Development Setup

For local development, you can run each service individually:

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies for a specific service:

   ```bash
   cd backend/{service-name} # Replace {service-name} with the service you want to run (ie. inference-service)
   pip install -r requirements.txt
   ```

3. Run the service:

   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

## Configuration ⚙️

Each service is configured through environment variables. Key configuration options include:

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

See the `.env.example` file in the deployments directory for a complete list of configuration options.

## API Documentation 📚

API documentation is available at:

- API Gateway: <http://localhost:8000/docs>
- Inference Service: <http://localhost:8001/docs>
- Agent Service: <http://localhost:8002/docs>
- Retrieval Service: <http://localhost:8003/docs>
- Chat Service: <http://localhost:8004/docs>

Each service provides a root endpoint (`/`) with information about available endpoints, and a Swagger UI documentation page at `/docs`.

## Deployment Options 🌐

### Docker Compose

For a complete deployment with all services:

```bash
cd backend/deployments
docker-compose up -d
```

### Kubernetes

Kubernetes manifests are available in the `deployments/kubernetes` directory:

```bash
kubectl apply -f deployments/kubernetes/
```

### Production Deployment

For production environments:

1. Configure production settings:

   ```bash
   cp deployments/.env.example deployments/.env.production
   # Edit .env.production with secure credentials
   ```

2. Deploy with SSL support:

   ```bash
   cd deployments
   ./deploy.sh production
   ```

## Security 🔒

- All API endpoints require authentication via JWT tokens
- Role-based access control for granular permissions
- Secure password hashing
- HTTPS/TLS encryption for production deployments

## Testing 🧪

### Running Tests

Each service includes unit tests using pytest. To run tests for a specific service:

```bash
cd backend/<service-name>
pytest
```

### Testing Individual Services

For development and testing, you can use the provided test scripts to run services individually:

```bash
cd backend/tests
./test-service.sh <service-name>
```

Available services:

- `api-gateway` (port 8000)
- `inference-service` (port 8001)
- `agent-service` (port 8002)
- `retrieval-service` (port 8003)
- `chat-service` (port 8004)

### Running All Services Locally

To run all services simultaneously for local development:

```bash
cd backend/tests
./run-all-services.sh
```

### Testing Deployments

After deploying with Docker Compose, you can verify the deployment with:

```bash
cd backend/deployments
./test-deployment.sh
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure that your code passes all tests before submitting a pull request.

## License 📜

This project is licensed under the BSD-3-Clause License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you have any questions, suggestions, or need assistance, please open an issue or join our community to connect with us!

## Troubleshooting

If you encounter issues:

1. Check that the required dependencies are installed:

   ```bash
   pip install -r backend/<service-name>/requirements.txt
   ```

2. Verify that service ports are not already in use:

   ```bash
   lsof -i :<port>
   ```

3. Check the logs for error messages.

4. Ensure PostgreSQL is running if using the chat-service with database functionality.

   ```bash
   # For local development with SQLite
   cd chat-service
   python -m alembic upgrade head

   # For production with PostgreSQL
   export DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   cd chat-service
   python -m alembic upgrade head
   ```

5. Verify environment variables are correctly set in your .env file.

---

Created with ❤️ by the Open WebUI team.
