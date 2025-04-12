#!/bin/bash

# Test script for the chat service

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
            curl -s -X "$method" "$API_URL$endpoint"
        else
            curl -s -X "$method" "$API_URL$endpoint" -H "Authorization: $auth_header"
        fi
    else
        if [ -z "$auth_header" ]; then
            curl -s -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -d "$data"
        else
            curl -s -X "$method" "$API_URL$endpoint" -H "Content-Type: application/json" -H "Authorization: $auth_header" -d "$data"
        fi
    fi
    echo -e "\n"
}

# First, we need to get a JWT token
echo "Getting JWT token..."
TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" -H "Content-Type: application/json" -d '{
  "username": "admin",
  "password": "admin"
}')
echo "Token response: $TOKEN_RESPONSE"

# Extract the token (this is a simplified approach)
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Token: $TOKEN"

if [ -z "$TOKEN" ]; then
    echo "Failed to get token. Using a dummy token for testing."
    TOKEN="dummy-token"
fi

# Create a chat
echo -e "\nCreating a chat..."
CHAT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/chat/chats" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{
  "title": "Test Chat with Phi",
  "models": [
    {
      "id": "phi:latest",
      "name": "phi:latest"
    }
  ],
  "system": "You are a helpful assistant."
}')
echo "Chat response: $CHAT_RESPONSE"

# Extract the chat ID
CHAT_ID=$(echo $CHAT_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Chat ID: $CHAT_ID"

if [ -z "$CHAT_ID" ]; then
    echo "Failed to create chat. Exiting."
    exit 1
fi

# Send a message to the chat
echo -e "\nSending a message to the chat..."
MESSAGE_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/chat/messages" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{
  "chat_id": "'$CHAT_ID'",
  "content": "Hello, how are you today?",
  "role": "user",
  "model": "phi:latest"
}')
echo "Message response: $MESSAGE_RESPONSE"

# Extract the message ID
MESSAGE_ID=$(echo $MESSAGE_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Message ID: $MESSAGE_ID"

if [ -z "$MESSAGE_ID" ]; then
    echo "Failed to send message. Exiting."
    exit 1
fi

# Get a response from the model
echo -e "\nGetting a response from the model..."
RESPONSE=$(curl -s -X POST "$API_URL/api/v1/inference/ollama/chat" -H "Content-Type: application/json" -d '{
  "model": "phi:latest",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello, how are you today?"
    }
  ],
  "stream": false
}')
echo "Response: $RESPONSE"

# Extract the assistant's message
ASSISTANT_MESSAGE=$(echo $RESPONSE | grep -o '"content":"[^"]*' | cut -d'"' -f4)
echo "Assistant message: $ASSISTANT_MESSAGE"

# Save the assistant's response to the chat
echo -e "\nSaving the assistant's response to the chat..."
ASSISTANT_RESPONSE=$(curl -s -X POST "$API_URL/api/v1/chat/messages" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{
  "chat_id": "'$CHAT_ID'",
  "content": "'"$ASSISTANT_MESSAGE"'",
  "role": "assistant",
  "parent_id": "'$MESSAGE_ID'",
  "model": "phi:latest"
}')
echo "Assistant response: $ASSISTANT_RESPONSE"

# Get the chat history
echo -e "\nGetting the chat history..."
CHAT_HISTORY=$(curl -s -X GET "$API_URL/api/v1/chat/chats/$CHAT_ID" -H "Authorization: Bearer $TOKEN")
echo "Chat history: $CHAT_HISTORY"

echo -e "\nTest completed!"
