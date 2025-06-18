#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting Global Encounters App Deployment...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker Desktop first.${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    cat > .env << EOL
# Database Configuration
DATABASE_URL=postgresql+psycopg2://admin:admin@localhost:5432/postgres

# JWT Settings
JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_REFRESH_SECRET_KEY=7c3e1b9f2d5a8e4c6b0a3d7f9e2c5b8a1d4f7e0c3b6a9d2f5e8c1b4a7d0f3e6

# Application Settings
PORT=8000

# Frontend URLs
FRONTEND_URL=http://localhost:3000
FRONTEND_URL_HTTPS=https://localhost:3000
EOL
    echo -e "${GREEN}.env file created successfully${NC}"
fi

# Stop and remove existing container if it exists
if docker ps -a | grep -q global-encounters; then
    echo -e "${GREEN}Removing existing container...${NC}"
    docker rm -f global-encounters
fi

# Build the Docker image
echo -e "${GREEN}Building Docker image...${NC}"
docker build -t global-encounters-app .

# Run the container
echo -e "${GREEN}Starting container...${NC}"
docker run -d \
    --name global-encounters \
    -p 8000:8000 \
    --env-file .env \
    global-encounters-app

# Check if container is running
if docker ps | grep -q global-encounters; then
    echo -e "${GREEN}Deployment successful!${NC}"
    echo -e "${GREEN}Application is running at: http://localhost:8000${NC}"
    echo -e "${GREEN}API documentation is available at: http://localhost:8000/docs${NC}"
else
    echo -e "${RED}Deployment failed. Please check the logs:${NC}"
    docker logs global-encounters
fi 