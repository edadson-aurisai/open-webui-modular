# API Gateway

The API Gateway is the entry point for all client requests to Open WebUI microservices.

## Features

- Route forwarding to appropriate microservices
- Authentication and authorization
- Request validation
- Rate limiting
- CORS handling
- Session management

## API Endpoints

- `/api/v1/inference/*` - Inference service endpoints
- `/api/v1/agent/*` - Agent service endpoints
- `/api/v1/retrieval/*` - Retrieval service endpoints
- `/api/v1/chat/*` - Chat service endpoints

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
uvicorn app.main:app --reload --port 8000
```

### Environment Variables

- `INFERENCE_SERVICE_URL` - Inference service URL
- `AGENT_SERVICE_URL` - Agent service URL
- `RETRIEVAL_SERVICE_URL` - Retrieval service URL
- `CHAT_SERVICE_URL` - Chat service URL
- `JWT_SECRET_KEY` - JWT secret key
- `JWT_ALGORITHM` - JWT algorithm
- `JWT_EXPIRES_IN` - JWT expiration time in days

## Testing

Run tests with:

```bash
pytest
```

## Deployment

See the [Deployments README](../deployments/README.md) for deployment instructions.
