#!/bin/bash

# Lead Intel API Deployment Script
# Usage: ./deploy.sh [environment]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default environment
ENVIRONMENT=${1:-production}

echo -e "${BLUE}🚀 Starting Lead Intel API Deployment${NC}"
echo -e "${YELLOW}Environment: ${ENVIRONMENT}${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install it and try again."
    exit 1
fi

# Stop existing containers
print_status "Stopping existing containers..."
docker-compose down --remove-orphans

# Build the application
print_status "Building Docker image..."
docker-compose build --no-cache

# Start the services
print_status "Starting services..."
docker-compose up -d

# Wait for service to be healthy
print_status "Waiting for service to be healthy..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "Service is healthy!"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Service failed to become healthy within 60 seconds"
        docker-compose logs
        exit 1
    fi
    sleep 2
done

# Run health check
print_status "Running health check..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "Health check passed!"
else
    print_error "Health check failed!"
    docker-compose logs
    exit 1
fi

# Test the API
print_status "Testing API endpoint..."
if curl -f -X POST "http://localhost:8000/enrich_lead" \
    -H "Content-Type: application/json" \
    -d '{"college": "ADYPU", "city": "Pune", "state": "Maharashtra", "course": "BBA", "language": "Hindi"}' > /dev/null 2>&1; then
    print_status "API test passed!"
else
    print_error "API test failed!"
    docker-compose logs
    exit 1
fi

# Show service status
print_status "Deployment completed successfully!"
echo -e "${BLUE}📊 Service Status:${NC}"
docker-compose ps

echo -e "${BLUE}🌐 API Endpoints:${NC}"
echo -e "  Health Check: ${GREEN}http://localhost:8000/health${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "  Enrich Lead: ${GREEN}http://localhost:8000/enrich_lead${NC}"

echo -e "${BLUE}📝 Logs:${NC}"
echo -e "  View logs: ${GREEN}docker-compose logs -f${NC}"
echo -e "  Stop service: ${GREEN}docker-compose down${NC}"

print_status "Lead Intel API is now deployed and ready to use! 🎉" 