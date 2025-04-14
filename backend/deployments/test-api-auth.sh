#!/bin/bash

# API test script with authentication

# Set the base URL
API_URL="http://localhost:8000"

# Function to make API requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local auth_header=$4
    
    echo "Request: $method $API_URL$endpoint"
    if [ -z "$data" ]; then
        if [ -z "$auth_header" ]; then
            curl -v -X "$method" "$API_URL$endpoint"
        else
            curl -v -X "$method" "$API_URL$endpoint" -H "Authorization: $auth_header"
        fi
    else
        if [ -z "$auth_header" ]; then
            curl -v -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -d "$data"
        else
            curl -v -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -H "Authorization: $auth_header" -d "$data"
        fi
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

# Test tools endpoint with a dummy token
echo -e "\nTesting tools endpoint with a dummy token..."
make_request "GET" "/api/v1/agent/tools" "" "Bearer dummy-token"

echo -e "\nAPI tests completed!"
