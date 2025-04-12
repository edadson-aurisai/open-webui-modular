#!/bin/bash

# Script to run all backend services using uvicorn

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(grep -v '^#' backend/.env.dev | xargs)

# Function to start a service
start_service() {
    local service=$1
    local port=$2
    
    echo "Installing dependencies for $service..."
    pip install -r backend/$service/requirements.txt
    
    echo "Starting $service on port $port..."
    cd backend/$service
    uvicorn app.main:app --host 0.0.0.0 --port $port --reload &
    cd ../..
    sleep 2  # Give some time for the service to start
}

# Start all services in background
echo "Starting all services..."

# API Gateway
start_service api-gateway 8000

# Inference Service
start_service inference-service 8001

# Agent Service
start_service agent-service 8002

# Retrieval Service
start_service retrieval-service 8003

# Chat Service
start_service chat-service 8004

echo "All services started!"
echo "API Gateway: http://localhost:8000"
echo "Inference Service: http://localhost:8001"
echo "Agent Service: http://localhost:8002"
echo "Retrieval Service: http://localhost:8003"
echo "Chat Service: http://localhost:8004"

# Keep the script running
echo "Press Ctrl+C to stop all services"
wait
