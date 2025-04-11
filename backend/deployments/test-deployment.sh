#!/bin/bash

# Test script for Open WebUI microservices deployment

echo "Testing Open WebUI microservices deployment..."

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
  echo "Error: Docker Compose services are not running."
  echo "Please start the services with: docker-compose up -d"
  exit 1
fi

# Load environment variables
source .env

# Determine if we're in production or development mode
if [ -n "$DOMAIN_NAME" ] && [ "$DOMAIN_NAME" != "your-domain.com" ]; then
  # Production mode - test via nginx
  BASE_URL="https://$DOMAIN_NAME"
  INTERNAL_TEST=true
  echo "Testing in production mode with domain: $DOMAIN_NAME"
else
  # Development mode - test directly
  BASE_URL="http://localhost"
  INTERNAL_TEST=false
  echo "Testing in development mode"
fi

# Function to test service health
test_service_health() {
  local service_name=$1
  local endpoint=$2
  local port=$3

  echo -n "Testing $service_name health... "

  if [ "$INTERNAL_TEST" = true ]; then
    # For internal testing, use Docker network
    if docker-compose exec nginx curl -s http://$endpoint:$port/health | grep -q "healthy"; then
      echo "OK"
      return 0
    else
      echo "FAILED"
      echo "$service_name health check failed."
      return 1
    fi
  else
    # For external testing, use the exposed endpoints
    if [ "$service_name" = "API Gateway" ]; then
      # API Gateway is exposed through nginx
      if curl -s $BASE_URL/api/health | grep -q "healthy"; then
        echo "OK"
        return 0
      else
        echo "FAILED"
        echo "$service_name health check failed."
        return 1
      fi
    else
      # Other services are tested internally
      if docker-compose exec nginx curl -s http://$endpoint:$port/health | grep -q "healthy"; then
        echo "OK"
        return 0
      else
        echo "FAILED"
        echo "$service_name health check failed."
        return 1
      fi
    fi
  fi
}

# Test frontend
echo -n "Testing frontend... "
if curl -s -o /dev/null -w "%{http_code}" $BASE_URL | grep -q "200\|301\|302"; then
  echo "OK"
else
  echo "FAILED"
  echo "Frontend check failed."
  exit 1
fi

# Test services
test_service_health "API Gateway" "api-gateway" "8000" || exit 1
test_service_health "Inference Service" "inference-service" "8001" || exit 1
test_service_health "Agent Service" "agent-service" "8002" || exit 1
test_service_health "Retrieval Service" "retrieval-service" "8003" || exit 1
test_service_health "Chat Service" "chat-service" "8004" || exit 1

echo "All services are healthy!"
echo "Open WebUI microservices deployment is working correctly."
