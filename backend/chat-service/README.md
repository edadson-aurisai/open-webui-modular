# Chat Service

The Chat Service manages chat sessions and message history for Open WebUI.

## Features

- Chat session management
- Message storage and retrieval
- Chat history
- User preferences
- Chat metadata (tags, folders, etc.)

## API Endpoints

- `/api/v1/chats` - Chat management
- `/api/v1/messages` - Message management
- `/api/v1/folders` - Folder management
- `/api/v1/tags` - Tag management

## Development

### Prerequisites

- Python 3.11+
- PostgreSQL (for production)

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
uvicorn app.main:app --reload --port 8004
```

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_POOL_SIZE` - Database connection pool size
- `ENABLE_CHAT_HISTORY` - Enable chat history
- `ENABLE_CHAT_TEMPLATES` - Enable chat templates
- `ENABLE_CHAT_EXPORT` - Enable chat export
- `ENABLE_CHAT_SHARING` - Enable chat sharing
- `JWT_SECRET_KEY` - JWT secret key

## Testing

Run tests with:

```bash
pytest
```

## Deployment

See the [Deployments README](../deployments/README.md) for deployment instructions.
