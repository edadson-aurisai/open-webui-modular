# Deployment Guide for Open WebUI

This guide provides instructions for deploying the Open WebUI application in both development and production environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (for production deployment)
- SSL certificates (will be automatically obtained using Let's Encrypt)

## Development Deployment

For local development and testing, follow these steps:

1. Navigate to the deployments directory:
   ```
   cd backend/deployments
   ```

2. Deploy the application in development mode:
   ```
   ./deploy.sh development
   ```

3. Access the application at http://localhost

## Production Deployment

For production deployment with HTTPS, follow these steps:

1. Navigate to the deployments directory:
   ```
   cd backend/deployments
   ```

2. Edit the `.env.production` file and update the following values:
   - `JWT_SECRET_KEY`: Set to a secure random string
   - `POSTGRES_PASSWORD`: Set to a secure password
   - `OPENAI_API_KEYS`: Set to your OpenAI API key (if using OpenAI)
   - `DOMAIN_NAME`: Set to your domain name (e.g., example.com)
   - `EMAIL_ADDRESS`: Set to your email address (for Let's Encrypt)

3. Make sure your domain is pointing to the server where you're deploying the application.

4. Deploy the application in production mode:
   ```
   ./deploy.sh production
   ```
   This will:
   - Obtain SSL certificates using Let's Encrypt
   - Build and start all services
   - Configure HTTPS

5. Access the application at https://your-domain.com

## Environment Configuration

The application uses environment variables for configuration. These are defined in:

- `.env.development`: Development environment configuration
- `.env.production`: Production environment configuration

You can customize these files to adjust the application's behavior.

## SSL Certificates

SSL certificates are automatically obtained using Let's Encrypt when deploying in production mode. The certificates are stored in the `ssl` directory and are valid for 90 days. They will need to be renewed before they expire.

To manually renew the certificates, run:
```
./setup-ssl.sh
```

## Troubleshooting

If you encounter issues during deployment, check the following:

1. Make sure Docker and Docker Compose are installed and running.
2. Check the logs of individual services:
   ```
   docker-compose logs [service-name]
   ```
3. Ensure your domain is correctly pointing to your server's IP address.
4. Verify that ports 80 and 443 are open and accessible.

For more detailed troubleshooting, run the test script:
```
./test-deployment.sh
```
