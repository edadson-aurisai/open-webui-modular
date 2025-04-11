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

# Check if environment is specified
ENV=${1:-production}

# Check if .env file exists, create from example if not
if [ ! -f ".env.$ENV" ]; then
    echo "Error: .env.$ENV file not found."
    echo "Please create an .env.$ENV file with your configuration before continuing."
    exit 1
fi

# Copy the environment file to .env
echo "Using $ENV environment..."
cp .env.$ENV .env

# Check if SSL certificates exist for production
if [ "$ENV" = "production" ]; then
    source .env
    if [ ! -f "./ssl/live/$DOMAIN_NAME/fullchain.pem" ]; then
        echo "SSL certificates not found. Running setup-ssl.sh..."
        ./setup-ssl.sh
        if [ $? -ne 0 ]; then
            echo "Failed to set up SSL certificates. Exiting."
            exit 1
        fi
    fi
fi

# Build and start the services
echo "Building and starting services..."
docker-compose up --build -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 15

# Run the test script
echo "Running tests..."
./test-deployment.sh

echo "Deployment complete!"
if [ "$ENV" = "production" ]; then
    echo "Your application is available at: https://$DOMAIN_NAME"
else
    echo "Your application is available at: http://localhost"
fi
echo "To stop the services, run: docker-compose down"
