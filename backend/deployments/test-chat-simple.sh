#!/bin/bash

# Test script for directly testing the chat with Ollama (simplified)

# Set the base URL
API_URL="http://localhost:8000"

# Test Ollama chat endpoint with a simple conversation
echo "Testing Ollama chat with a simple conversation..."
curl -s -X POST "$API_URL/api/v1/inference/ollama/chat" \
  -H "Content-Type: application/json" \
  -d '{"model":"phi:latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello, how are you today?"}],"stream":false}'
echo -e "\n"

# Test Ollama chat endpoint with a more complex conversation
echo -e "\nTesting Ollama chat with a more complex conversation..."
curl -s -X POST "$API_URL/api/v1/inference/ollama/chat" \
  -H "Content-Type: application/json" \
  -d '{"model":"phi:latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello, how are you today?"},{"role":"assistant","content":"I am doing well, thank you for asking! How can I assist you today?"},{"role":"user","content":"Can you tell me about the solar system?"}],"stream":false}'
echo -e "\n"

echo -e "\nTest completed!"
