#!/bin/bash

# Test script for health endpoints

echo "Testing health endpoints..."

# API Gateway
echo -n "Testing API Gateway health... "
if curl -s http://localhost:8000/health | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "API Gateway health check failed."
  exit 1
fi

# Test other services through the API Gateway
echo -n "Testing Inference Service health... "
if docker-compose exec -T inference-service python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/health').read().decode())" | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Inference Service health check failed."
  exit 1
fi

echo -n "Testing Agent Service health... "
if docker-compose exec -T agent-service python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8002/health').read().decode())" | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Agent Service health check failed."
  exit 1
fi

echo -n "Testing Retrieval Service health... "
if docker-compose exec -T retrieval-service python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8003/health').read().decode())" | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Retrieval Service health check failed."
  exit 1
fi

echo -n "Testing Chat Service health... "
if docker-compose exec -T chat-service python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8004/health').read().decode())" | grep -q "healthy"; then
  echo "OK"
else
  echo "FAILED"
  echo "Chat Service health check failed."
  exit 1
fi

echo "All health checks passed!"
