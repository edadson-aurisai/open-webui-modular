#!/bin/bash

# Development script to run all microservices locally

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies for each service
echo "Installing dependencies for all services..."
pip install -r api-gateway/requirements.txt
pip install -r inference-service/requirements.txt
pip install -r agent-service/requirements.txt
pip install -r retrieval-service/requirements.txt
pip install -r chat-service/requirements.txt

# Start each service in a separate terminal
echo "Starting all services..."

# Function to start a service
start_service() {
    local service=$1
    local port=$2
    cd $service
    echo "Starting $service on port $port..."
    uvicorn app.main:app --reload --port $port &
    cd ..
}

# Start services
start_service api-gateway 8000
start_service inference-service 8001
start_service agent-service 8002
start_service retrieval-service 8003
start_service chat-service 8004

echo "All services started!"
echo "API Gateway: http://localhost:8000"
echo "Inference Service: http://localhost:8001"
echo "Agent Service: http://localhost:8002"
echo "Retrieval Service: http://localhost:8003"
echo "Chat Service: http://localhost:8004"

# Wait for user to press Ctrl+C
echo "Press Ctrl+C to stop all services"
trap "kill 0" EXIT
wait
