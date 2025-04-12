#!/bin/bash

# Test script for directly testing the chat with Ollama through the inference-service

# Set the base URL
API_URL="http://localhost:8001"

# Test Ollama chat endpoint with a simple conversation
echo "Testing Ollama chat with a simple conversation directly through the inference-service..."
curl -s -X POST "$API_URL/api/v1/ollama/chat" \
  -H "Content-Type: application/json" \
  -d '{"model":"phi:latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello, how are you today?"}],"stream":false}'
echo -e "\n"

echo -e "\nTest completed!"
