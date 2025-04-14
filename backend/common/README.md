# Common

This directory contains shared utilities, helpers, and schemas used across all Open WebUI microservices.

## Components

- `models/` - Shared Pydantic models
- `db/` - Database connection utilities
- `utils/` - Shared utility functions
- `middleware/` - Shared middleware
- `auth/` - Authentication utilities
- `config.py` - Configuration settings
- `constants.py` - Shared constants

## Usage

To use these shared components in a microservice, import them directly:

```python
from common.db import Base, Session, get_db
from common.models import BaseResponse, ErrorResponse
from common.utils import get_logger
from common.auth import get_current_user
from common.middleware import setup_cors
from common.config import get_service_config
from common.constants import ERROR_MESSAGES
```

## Development

When adding new shared components, make sure they are properly exported in the respective `__init__.py` files to make them easily importable.
