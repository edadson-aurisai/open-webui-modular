#!/bin/bash

# Script to test a specific backend service using uvicorn

# Check if service name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <service-name>"
    echo "Available services: api-gateway, chat-service, agent-service, inference-service, retrieval-service"
    exit 1
fi

SERVICE_NAME=$1

# Check if service directory exists
if [ ! -d "backend/$SERVICE_NAME" ]; then
    echo "Error: Service directory 'backend/$SERVICE_NAME' not found"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(grep -v '^#' backend/.env.dev | xargs)

# Install service dependencies
echo "Installing dependencies for $SERVICE_NAME..."
pip install -r backend/$SERVICE_NAME/requirements.txt
pip install -r backend/common/requirements.txt

# Determine port based on service name
case $SERVICE_NAME in
    "api-gateway")
        PORT=8000
        ;;
    "chat-service")
        PORT=8001
        ;;
    "agent-service")
        PORT=8002
        ;;
    "inference-service")
        PORT=8003
        ;;
    "retrieval-service")
        PORT=8004
        ;;
    *)
        echo "Unknown service: $SERVICE_NAME"
        exit 1
        ;;
esac

# Run the service with uvicorn
echo "Starting $SERVICE_NAME on port $PORT..."
cd backend/$SERVICE_NAME
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
