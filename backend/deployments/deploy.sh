#!/bin/bash

# Deployment script for Open WebUI microservices

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Check if .env file exists, create from example if not
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit the .env file with your configuration before continuing."
    echo "Press Enter to continue or Ctrl+C to exit."
    read
fi

# Build and start the services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Run the test script
echo "Running tests..."
./test-deployment.sh

echo "Deployment complete!"
echo "API Gateway is available at: http://localhost:8000"
echo "To stop the services, run: docker-compose down"
