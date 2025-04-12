#!/bin/bash

# Test script for testing chat history with Ollama

# Set the base URL
API_URL="http://localhost:8000"

# Step 1: Create a chat with Ollama
echo "Step 1: Creating a chat with Ollama..."
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/inference/ollama/chat" \
  -H "Content-Type: application/json" \
  -d '{"model":"phi:latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello, how are you today?"}],"stream":false}')
echo "$CHAT_RESPONSE"
echo -e "\n"

# Extract the assistant's message
ASSISTANT_MESSAGE=$(echo "$CHAT_RESPONSE" | grep -o '"content":"[^"]*' | cut -d'"' -f4)
echo "Assistant message: $ASSISTANT_MESSAGE"
echo -e "\n"

# Step 2: Send a follow-up message
echo "Step 2: Sending a follow-up message..."
FOLLOW_UP_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/inference/ollama/chat" \
  -H "Content-Type: application/json" \
  -d '{"model":"phi:latest","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello, how are you today?"},{"role":"assistant","content":"'"$ASSISTANT_MESSAGE"'"},{"role":"user","content":"Tell me a joke."}],"stream":false}')
echo "$FOLLOW_UP_RESPONSE"
echo -e "\n"

echo "Test completed!"
