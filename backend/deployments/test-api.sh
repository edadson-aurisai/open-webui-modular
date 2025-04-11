#!/bin/bash

# API test script for Open WebUI microservices

# Set the base URL
API_URL="http://localhost:8000"

# Function to make API requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -z "$data" ]; then
        curl -s -X "$method" "$API_URL$endpoint" | jq .
    else
        curl -s -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -d "$data" | jq .
    fi
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install jq for better output formatting."
    echo "Continuing without jq..."
    
    # Redefine make_request without jq
    make_request() {
        local method=$1
        local endpoint=$2
        local data=$3
        
        if [ -z "$data" ]; then
            curl -s -X "$method" "$API_URL$endpoint"
        else
            curl -s -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -d "$data"
        fi
    }
fi

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
