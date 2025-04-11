#!/bin/bash

# Test script for Open WebUI microservices deployment

echo "Testing Open WebUI microservices deployment..."

# Check if Docker Compose is running
if ! docker-compose ps | grep -q "Up"; then
  echo "Error: Docker Compose services are not running."
  echo "Please start the services with: docker-compose up -d"
  exit 1
fi

# Test API Gateway health
echo -n "Testing API Gateway health... "
if curl -s http://localhost:8000/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "API Gateway health check failed."
  exit 1
fi

# Test Inference Service health
echo -n "Testing Inference Service health... "
if curl -s http://localhost:8001/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Inference Service health check failed."
  exit 1
fi

# Test Agent Service health
echo -n "Testing Agent Service health... "
if curl -s http://localhost:8002/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Agent Service health check failed."
  exit 1
fi

# Test Retrieval Service health
echo -n "Testing Retrieval Service health... "
if curl -s http://localhost:8003/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Retrieval Service health check failed."
  exit 1
fi

# Test Chat Service health
echo -n "Testing Chat Service health... "
if curl -s http://localhost:8004/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Chat Service health check failed."
  exit 1
fi

echo "All services are healthy!"
echo "Open WebUI microservices deployment is working correctly."
