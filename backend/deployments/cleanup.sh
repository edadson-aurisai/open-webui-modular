#!/bin/bash

# Cleanup script for Open WebUI microservices

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Stop the services
echo "Stopping services..."
docker-compose down

# Ask if volumes should be removed
echo "Do you want to remove all data volumes? This will delete all database data, uploaded files, and models. (y/N)"
read -r remove_volumes

if [[ $remove_volumes =~ ^[Yy]$ ]]; then
    echo "Removing volumes..."
    docker volume rm deployments_postgres-data deployments_retrieval-data deployments_chroma-data deployments_ollama-data
    echo "Volumes removed."
else
    echo "Volumes preserved."
fi

echo "Cleanup complete!"
