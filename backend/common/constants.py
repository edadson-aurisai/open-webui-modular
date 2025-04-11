"""
Common constants used across all microservices
"""

# Error messages
class ERROR_MESSAGES:
    DEFAULT = lambda: "An error occurred"
    NOT_FOUND = "Resource not found"
    ACCESS_PROHIBITED = "Access prohibited"
    INVALID_CREDENTIALS = "Invalid credentials"
    INVALID_TOKEN = "Invalid token"
    EXPIRED_TOKEN = "Expired token"
    INVALID_REQUEST = "Invalid request"
    INTERNAL_SERVER_ERROR = "Internal server error"
    SERVICE_UNAVAILABLE = "Service unavailable"


# User roles
class USER_ROLES:
    ADMIN = "admin"
    USER = "user"
    PENDING = "pending"


# Model providers
class MODEL_PROVIDERS:
    OLLAMA = "ollama"
    OPENAI = "openai"
    ARENA = "arena"
