#!/bin/bash

# Script to set up SSL certificates using Let's Encrypt

# Load environment variables
source .env.production

# Check if domain name is set
if [ -z "$DOMAIN_NAME" ]; then
    echo "Error: DOMAIN_NAME is not set in .env.production"
    exit 1
fi

# Check if email address is set
if [ -z "$EMAIL_ADDRESS" ]; then
    echo "Error: EMAIL_ADDRESS is not set in .env.production"
    exit 1
fi

# Create directories for SSL certificates
mkdir -p ./ssl/live/$DOMAIN_NAME
mkdir -p ./nginx/certbot

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

# Run Certbot to obtain SSL certificates
echo "Obtaining SSL certificates for $DOMAIN_NAME..."
docker run -it --rm \
    -v ./ssl:/etc/letsencrypt \
    -v ./nginx/certbot:/var/www/certbot \
    certbot/certbot certonly --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL_ADDRESS \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN_NAME

# Check if certificates were obtained successfully
if [ $? -ne 0 ]; then
    echo "Failed to obtain SSL certificates."
    exit 1
fi

echo "SSL certificates obtained successfully!"
echo "You can now deploy your application with HTTPS enabled."
echo "To deploy, run: ./deploy.sh"
