# Open WebUI API Documentation

This document provides detailed API documentation for all Open WebUI microservices.

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [API Gateway](#api-gateway)
- [Chat Service](#chat-service)
- [Inference Service](#inference-service)
- [Agent Service](#agent-service)
- [Retrieval Service](#retrieval-service)

## Overview

The Open WebUI backend is built as a set of microservices, each with its own API endpoints. All client requests are routed through the API Gateway, which forwards them to the appropriate service.

## Authentication

All API endpoints require authentication via JWT tokens, except for public endpoints like registration, login, and public chat sharing.

**Headers**:

```
Authorization: Bearer <jwt_token>
```

## API Gateway

The API Gateway serves as the entry point for all client requests. It handles authentication, request validation, and routing to the appropriate microservice.

Base URL: `/api/v1`

## Chat Service

The Chat Service manages chat sessions and message history.

Base URL: `/api/v1/chats`

### Endpoints

#### List Chats

```
GET /api/v1/chats
```

**Query Parameters**:

- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of chats per page (default: 50)

**Response**:

```json
{
  "chats": [
    {
      "id": "string",
      "title": "string",
      "updated_at": "datetime",
      "created_at": "datetime",
      "pinned": false,
      "folder_id": "string",
      "tags": ["string"]
    }
  ]
}
```

#### Create Chat

```
POST /api/v1/chats
```

**Request Body**:

```json
{
  "title": "string",
  "models": [{"id": "string", "parameters": {}}],
  "system": "string",
  "tags": ["string"],
  "messages": []
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Get Chat

```
GET /api/v1/chats/{chat_id}
```

**Path Parameters**:

- `chat_id`: ID of the chat

**Response**:

```json
{
  "id": "string",
  "title": "string",
  "user_id": "string",
  "models": [{"id": "string", "parameters": {}}],
  "system": "string",
  "messages": [],
  "created_at": "datetime",
  "updated_at": "datetime",
  "share_id": "string",
  "archived": false,
  "pinned": false,
  "folder_id": "string",
  "tags": ["string"]
}
```

#### Update Chat

```
PUT /api/v1/chats/{chat_id}
```

**Path Parameters**:

- `chat_id`: ID of the chat

**Request Body**:

```json
{
  "title": "string",
  "models": [{"id": "string", "parameters": {}}],
  "system": "string",
  "tags": ["string"],
  "messages": []
}
```

**Response**:

```json
{
  "id": "string",
  "title": "string",
  "user_id": "string",
  "models": [{"id": "string", "parameters": {}}],
  "system": "string",
  "messages": [],
  "created_at": "datetime",
  "updated_at": "datetime",
  "share_id": "string",
  "archived": false,
  "pinned": false,
  "folder_id": "string",
  "tags": ["string"]
}
```

#### Delete Chat

```
DELETE /api/v1/chats/{chat_id}
```

**Path Parameters**:

- `chat_id`: ID of the chat

**Response**:

```json
true
```

#### Share Chat

```
POST /api/v1/chats/{chat_id}/share
```

**Path Parameters**:

- `chat_id`: ID of the chat

**Response**:

```
"share_id_string"
```

### Messages API

Base URL: `/api/v1/messages`

#### List Messages

```
GET /api/v1/messages
```

**Query Parameters**:

- `chat_id`: ID of the chat
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of messages per page (default: 50)

**Response**:

```json
{
  "messages": [
    {
      "id": "string",
      "chat_id": "string",
      "role": "user|assistant|system",
      "content": "string",
      "created_at": "datetime"
    }
  ]
}
```

#### Create Message

```
POST /api/v1/messages
```

**Request Body**:

```json
{
  "chat_id": "string",
  "role": "user|assistant|system",
  "content": "string"
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Update Message

```
PUT /api/v1/messages/{message_id}
```

**Path Parameters**:

- `message_id`: ID of the message

**Request Body**:

```json
{
  "content": "string"
}
```

**Response**:

```json
{
  "id": "string",
  "chat_id": "string",
  "role": "user|assistant|system",
  "content": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Delete Message

```
DELETE /api/v1/messages/{message_id}
```

**Path Parameters**:

- `message_id`: ID of the message

**Response**:

```json
true
```

### Folders API

Base URL: `/api/v1/folders`

#### List Folders

```
GET /api/v1/folders
```

**Response**:

```json
{
  "folders": [
    {
      "id": "string",
      "name": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```

#### Create Folder

```
POST /api/v1/folders
```

**Request Body**:

```json
{
  "name": "string"
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Update Folder

```
PUT /api/v1/folders/{folder_id}
```

**Path Parameters**:

- `folder_id`: ID of the folder

**Request Body**:

```json
{
  "name": "string"
}
```

**Response**:

```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Delete Folder

```
DELETE /api/v1/folders/{folder_id}
```

**Path Parameters**:

- `folder_id`: ID of the folder

**Response**:

```json
true
```

### Tags API

Base URL: `/api/v1/tags`

#### List Tags

```
GET /api/v1/tags
```

**Response**:

```json
{
  "tags": [
    {
      "id": "string",
      "name": "string",
      "color": "string",
      "created_at": "datetime"
    }
  ]
}
```

#### Create Tag

```
POST /api/v1/tags
```

**Request Body**:

```json
{
  "name": "string",
  "color": "string"
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Update Tag

```
PUT /api/v1/tags/{tag_id}
```

**Path Parameters**:

- `tag_id`: ID of the tag

**Request Body**:

```json
{
  "name": "string",
  "color": "string"
}
```

**Response**:

```json
{
  "id": "string",
  "name": "string",
  "color": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Delete Tag

```
DELETE /api/v1/tags/{tag_id}
```

**Path Parameters**:

- `tag_id`: ID of the tag

**Response**:

```json
true
```

## Inference Service

The Inference Service handles LLM model inference, supporting multiple model providers including OpenAI-compatible APIs and Ollama.

Base URL: `/api/v1/inference`

### Models API

Base URL: `/api/v1/inference/models`

#### List Models

```
GET /api/v1/inference/models
```

**Response**:

```json
[
  {
    "id": "string",
    "name": "string",
    "owned_by": "string",
    "base_model_id": "string",
    "params": {
      "context_length": 4096,
      "embedding_size": 768,
      "quantization_level": "q4_0",
      "model_format": "gguf",
      "model_family": "string",
      "model_families": ["string"],
      "parameter_size": "7B"
    },
    "meta": {
      "description": "string",
      "license": "string",
      "tags": ["string"],
      "access_control": {}
    },
    "created_at": 1628150400,
    "updated_at": 1628150400
  }
]
```

#### List Base Models

```
GET /api/v1/inference/models/base
```

**Response**:

```json
[
  {
    "id": "string",
    "name": "string",
    "owned_by": "string",
    "base_model_id": null,
    "params": {
      "context_length": 4096,
      "embedding_size": 768,
      "quantization_level": null,
      "model_format": "gguf",
      "model_family": "string",
      "model_families": ["string"],
      "parameter_size": "7B"
    },
    "meta": {
      "description": "string",
      "license": "string",
      "tags": ["string"],
      "access_control": {}
    },
    "created_at": 1628150400,
    "updated_at": 1628150400
  }
]
```

### OpenAI-Compatible API

Base URL: `/api/v1/inference/openai`

#### Chat Completions

```
POST /api/v1/inference/openai/chat/completions
```

**Request Body**:

```json
{
  "model": "string",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string"
    }
  ],
  "temperature": 0.7,
  "top_p": 1.0,
  "n": 1,
  "stream": false,
  "max_tokens": 256,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "idx": 0
}
```

**Response** (when `stream=false`):

```json
{
  "id": "string",
  "object": "chat.completion",
  "created": 1628150400,
  "model": "string",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "string"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

For streaming responses (`stream=true`), the API returns a stream of server-sent events.

#### Completions

```
POST /api/v1/inference/openai/completions
```

**Request Body**:

```json
{
  "model": "string",
  "prompt": "string",
  "temperature": 0.7,
  "top_p": 1.0,
  "n": 1,
  "stream": false,
  "max_tokens": 256,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "idx": 0
}
```

**Response** (when `stream=false`):

```json
{
  "id": "string",
  "object": "text_completion",
  "created": 1628150400,
  "model": "string",
  "choices": [
    {
      "text": "string",
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

#### OpenAI Proxy

The service also provides a proxy to the OpenAI API for all other OpenAI API endpoints:

```
{HTTP_METHOD} /api/v1/inference/openai/{path}
```

Where `{path}` is any valid OpenAI API path and `{HTTP_METHOD}` is any of GET, POST, PUT, DELETE.

**Query Parameters**:
- `idx` (optional): Index of the OpenAI API key to use (default: 0)

### Ollama API

Base URL: `/api/v1/inference/ollama`

#### Generate

```
POST /api/v1/inference/ollama/generate
```

**Request Body**:
```json
{
  "model": "string",
  "prompt": "string",
  "stream": false,
  "options": {
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 40,
    "num_predict": 256
  }
}
```

**Response** (when `stream=false`):
```json
{
  "model": "string",
  "response": "string",
  "done": true,
  "context": [123, 456, 789],
  "total_duration": 1234567890,
  "load_duration": 123456789,
  "prompt_eval_count": 12,
  "prompt_eval_duration": 123456789,
  "eval_count": 25,
  "eval_duration": 123456789
}
```

#### Chat

```
POST /api/v1/inference/ollama/chat
```

**Request Body**:
```json
{
  "model": "string",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string"
    }
  ],
  "stream": false,
  "options": {
    "temperature": 0.7,
    "top_p": 1.0,
    "top_k": 40,
    "num_predict": 256
  }
}
```

**Response** (when `stream=false`):
```json
{
  "model": "string",
  "message": {
    "role": "assistant",
    "content": "string"
  },
  "done": true
}
```

For streaming responses (`stream=true`), the API returns a stream of server-sent events.

#### Completion

```
POST /api/v1/inference/ollama/api/completion
```

**Request Body**:
```json
{
  "model": "string",
  "prompt": "string",
  "stream": false,
  "temperature": 0.7,
  "top_p": 1.0,
  "top_k": 40,
  "max_tokens": 256
}
```

**Response** (when `stream=false`):
```json
{
  "id": "string",
  "object": "text_completion",
  "created": 1628150400,
  "model": "string",
  "choices": [
    {
      "text": "string",
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

#### Chat Completion

```
POST /api/v1/inference/ollama/api/chat/completion
```

**Request Body**:
```json
{
  "model": "string",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string"
    }
  ],
  "stream": false,
  "temperature": 0.7,
  "top_p": 1.0,
  "top_k": 40,
  "max_tokens": 256
}
```

**Response** (when `stream=false`):
```json
{
  "id": "string",
  "object": "chat.completion",
  "created": 1628150400,
  "model": "string",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "string"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

## Agent Service

The Agent Service orchestrates agents and multi-step workflows.

Base URL: `/api/v1/agents`

### Tools API

Base URL: `/api/v1/agents/tools`

#### List Tools

```
GET /api/v1/agents/tools
```

**Response**:
```json
{
  "tools": [
    {
      "name": "string",
      "description": "string",
      "spec": {
        "name": "string",
        "description": "string",
        "parameters": {},
        "returns": {}
      },
      "server": {}
    }
  ]
}
```

#### Execute Tool

```
POST /api/v1/agents/tools/execute
```

**Request Body**:

```json
{
  "tool_name": "string",
  "params": {}
}
```

**Response**:

```json
{
  "result": {}
}
```

### Tasks API

Base URL: `/api/v1/agents/tasks`

#### List Tasks

```
GET /api/v1/agents/tasks
```

**Query Parameters**:

- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of tasks per page (default: 50)

**Response**:

```json
{
  "tasks": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "status": "pending|running|completed|failed",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```

#### Create Task

```
POST /api/v1/agents/tasks
```

**Request Body**:

```json
{
  "name": "string",
  "description": "string",
  "pipeline_id": "string",
  "inputs": {}
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Get Task

```
GET /api/v1/agents/tasks/{task_id}
```

**Path Parameters**:

- `task_id`: ID of the task

**Response**:

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "pipeline_id": "string",
  "status": "pending|running|completed|failed",
  "inputs": {},
  "outputs": {},
  "logs": [
    {
      "timestamp": "datetime",
      "level": "info|warning|error",
      "message": "string"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Cancel Task

```
POST /api/v1/agents/tasks/{task_id}/cancel
```

**Path Parameters**:

- `task_id`: ID of the task

**Response**:

```json
true
```

### Pipelines API

Base URL: `/api/v1/agents/pipelines`

#### List Pipelines

```
GET /api/v1/agents/pipelines
```

**Response**:

```json
{
  "pipelines": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```

#### Create Pipeline

```
POST /api/v1/agents/pipelines
```

**Request Body**:

```json
{
  "name": "string",
  "description": "string",
  "config": {
    "nodes": [
      {
        "id": "string",
        "type": "string",
        "config": {}
      }
    ],
    "edges": [
      {
        "source": "string",
        "target": "string"
      }
    ]
  }
}
```

**Response**:

```json
{
  "id": "string"
}
```

#### Get Pipeline

```
GET /api/v1/agents/pipelines/{pipeline_id}
```

**Path Parameters**:

- `pipeline_id`: ID of the pipeline

**Response**:

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "config": {
    "nodes": [
      {
        "id": "string",
        "type": "string",
        "config": {}
      }
    ],
    "edges": [
      {
        "source": "string",
        "target": "string"
      }
    ]
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Update Pipeline

```
PUT /api/v1/agents/pipelines/{pipeline_id}
```

**Path Parameters**:

- `pipeline_id`: ID of the pipeline

**Request Body**:

```json
{
  "name": "string",
  "description": "string",
  "config": {
    "nodes": [
      {
        "id": "string",
        "type": "string",
        "config": {}
      }
    ],
    "edges": [
      {
        "source": "string",
        "target": "string"
      }
    ]
  }
}
```

**Response**:
```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "config": {
    "nodes": [
      {
        "id": "string",
        "type": "string",
        "config": {}
      }
    ],
    "edges": [
      {
        "source": "string",
        "target": "string"
      }
    ]
  },
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### Delete Pipeline

```
DELETE /api/v1/agents/pipelines/{pipeline_id}
```

**Path Parameters**:
- `pipeline_id`: ID of the pipeline

**Response**:
```json
true
```

#### Execute Pipeline

```
POST /api/v1/agents/pipelines/{pipeline_id}/execute
```

**Path Parameters**:
- `pipeline_id`: ID of the pipeline

**Request Body**:
```json
{
  "inputs": {}
}
```

**Response**:
```json
{
  "task_id": "string"
}
```

### Code Execution API

Base URL: `/api/v1/agents/code`

#### Execute Code

```
POST /api/v1/agents/code/execute
```

**Request Body**:
```json
{
  "language": "python|javascript|bash",
  "code": "string",
  "timeout": 30
}
```

**Response**:
```json
{
  "result": "string",
  "stdout": "string",
  "stderr": "string",
  "execution_time": 0.123
}
```

## Retrieval Service

The Retrieval Service performs vector/keyword search and document retrieval.

Base URL: `/api/v1/retrieval`

### Vector API

Base URL: `/api/v1/retrieval/vector`

#### Search Vectors

```
POST /api/v1/retrieval/vector/search
```

**Request Body**:
```json
{
  "collection_name": "string",
  "query": "string",
  "k": 10,
  "filter": {}
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "string",
      "score": 0.95,
      "metadata": {},
      "content": "string"
    }
  ]
}
```

#### Upsert Vectors

```
POST /api/v1/retrieval/vector/upsert
```

**Request Body**:
```json
{
  "collection_name": "string",
  "texts": ["string"],
  "metadatas": [{}],
  "ids": ["string"]
}
```

**Response**:
```json
{
  "ids": ["string"]
}
```

#### Delete Vectors

```
POST /api/v1/retrieval/vector/delete
```

**Request Body**:
```json
{
  "collection_name": "string",
  "ids": ["string"],
  "filter": {}
}
```

**Response**:
```json
{
  "success": true
}
```

#### Get Embedding

```
POST /api/v1/retrieval/vector/embedding
```

**Query Parameters**:
- `text`: Text to get embedding for

**Response**:
```json
{
  "embedding": [0.1, 0.2, 0.3, ...]
}
```

### Files API

Base URL: `/api/v1/retrieval/files`

#### Upload File

```
POST /api/v1/retrieval/files/upload
```

**Form Data**:
- `file`: File to upload
- `collection_name`: Collection name to store the file in

**Response**:
```json
{
  "id": "string",
  "filename": "string",
  "document_ids": ["string"]
}
```

#### List Files

```
GET /api/v1/retrieval/files/list
```

**Query Parameters**:
- `collection_name` (optional): Collection name to filter by

**Response**:
```json
{
  "files": [
    {
      "id": "string",
      "filename": "string",
      "collection_name": "string",
      "created_at": "datetime"
    }
  ]
}
```

#### Delete File

```
DELETE /api/v1/retrieval/files/{file_id}
```

**Path Parameters**:
- `file_id`: ID of the file to delete

**Response**:
```json
{
  "success": true
}
```

### Knowledge API

Base URL: `/api/v1/retrieval/knowledge`

#### Search Knowledge

```
POST /api/v1/retrieval/knowledge/search
```

**Request Body**:
```json
{
  "query": "string",
  "collection_name": "string",
  "k": 10,
  "filter": {}
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "string",
      "score": 0.95,
      "content": "string",
      "metadata": {
        "source": "string",
        "page": 1
      }
    }
  ]
}
```

#### Get Collections

```
GET /api/v1/retrieval/knowledge/collections
```

**Response**:
```json
{
  "collections": ["string"]
}
```

#### Create Collection

```
POST /api/v1/retrieval/knowledge/collections
```

**Request Body**:
```json
{
  "name": "string"
}
```

**Response**:
```json
{
  "name": "string"
}
```

#### Delete Collection

```
DELETE /api/v1/retrieval/knowledge/collections/{name}
```

**Path Parameters**:
- `name`: Name of the collection to delete

**Response**:
```json
{
  "success": true
}
```

### Web API

Base URL: `/api/v1/retrieval/web`

#### Scrape URL

```
POST /api/v1/retrieval/web/scrape
```

**Request Body**:
```json
{
  "url": "string",
  "collection_name": "string"
}
```

**Response**:
```json
{
  "success": true,
  "document_ids": ["string"]
}
```

#### Search Web

```
POST /api/v1/retrieval/web/search
```

**Request Body**:
```json
{
  "query": "string",
  "num_results": 5
}
```

**Response**:
```json
{
  "results": [
    {
      "title": "string",
      "url": "string",
      "snippet": "string"
    }
  ]
}
``` 