# Retrieval Service

The Retrieval Service performs vector/keyword search and document retrieval for Open WebUI.

## Features

- Vector database integration (Chroma, Milvus, Qdrant, etc.)
- Document processing
- Embedding generation
- Web search integration
- RAG implementation

## API Endpoints

- `/api/v1/vector` - Vector search and management
- `/api/v1/web` - Web search and content fetching
- `/api/v1/files` - File upload and management
- `/api/v1/knowledge` - Knowledge base management

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

- `VECTOR_DB` - Vector database type (chroma, milvus, qdrant, etc.)
- `VECTOR_DB_URL` - Vector database URL
- `VECTOR_DB_API_KEY` - Vector database API key
- `EMBEDDING_MODEL` - Embedding model name
- `EMBEDDING_ENGINE` - Embedding engine (ollama, openai, etc.)
- `EMBEDDING_BATCH_SIZE` - Embedding batch size
- `ENABLE_RAG_HYBRID_SEARCH` - Enable hybrid search
- `ENABLE_RAG_LOCAL_WEB_FETCH` - Enable local web fetch
- `ENABLE_RAG_WEB_SEARCH` - Enable web search
- `RAG_WEB_SEARCH_ENGINE` - Web search engine
- `UPLOAD_DIR` - Upload directory
- `JWT_SECRET_KEY` - JWT secret key

## Testing

Run tests with:

```bash
pytest
```

## Deployment

See the [Deployments README](../deployments/README.md) for deployment instructions.
