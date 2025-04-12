#!/bin/bash

# API test script for Open WebUI microservices (raw output)

# Set the base URL
API_URL="http://localhost:8000"

# Function to make API requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    echo "Request: $method $API_URL$endpoint"
    if [ -z "$data" ]; then
        curl -v -X "$method" "$API_URL$endpoint"
    else
        curl -v -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -d "$data"
    fi
    echo -e "\n"
}

# Test health endpoint
echo "Testing health endpoint..."
make_request "GET" "/health"

# Test API endpoints
echo -e "\nTesting API endpoints..."

# Test models endpoint
echo -e "\nTesting models endpoint..."
make_request "GET" "/api/v1/inference/models"

# Test tools endpoint
echo -e "\nTesting tools endpoint..."
make_request "GET" "/api/v1/agent/tools"

echo -e "\nAPI tests completed!"
