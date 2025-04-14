#!/bin/bash

# Test script for Open WebUI backend microservices

echo "Testing Open WebUI backend microservices..."

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
  echo "Error: Docker Compose services are not running."
  echo "Please start the services with: docker-compose up -d"
  exit 1
fi

# Load environment variables
source .env

# Function to test service health directly
test_service_health() {
  local service_name=$1
  local endpoint=$2
  local port=$3

  echo -n "Testing $service_name health... "

  # Test directly using Docker exec
  if docker-compose exec api-gateway curl -s http://$endpoint:$port/health | grep -q "healthy"; then
    echo "OK"
    return 0
  else
    echo "FAILED"
    echo "$service_name health check failed."
    return 1
  fi
}

# Test services
test_service_health "API Gateway" "api-gateway" "8000" || exit 1
test_service_health "Inference Service" "inference-service" "8001" || exit 1
test_service_health "Agent Service" "agent-service" "8002" || exit 1
test_service_health "Retrieval Service" "retrieval-service" "8003" || exit 1
test_service_health "Chat Service" "chat-service" "8004" || exit 1

echo "All backend services are healthy!"
echo "Open WebUI backend microservices are working correctly."
