#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Global Encounters App Deployment...${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Azure CLI is not installed. Please install it first:${NC}"
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install it first:${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo -e "${RED}No .env file found. Creating one...${NC}"
    cat > .env << EOL
DATABASE_URL=postgresql+psycopg2://admin:admin@52.168.133.23:5432/postgres
JWT_SECRET_KEY=$(openssl rand -hex 32)
PORT=8000
EOL
    echo -e "${GREEN}Created .env file with default values${NC}"
fi

# Azure login
echo -e "${GREEN}Logging into Azure...${NC}"
az login

# Set variables
read -p "Enter your desired Azure Container Registry name (lowercase, no spaces): " ACR_NAME
read -p "Enter your desired App Service name (lowercase, no spaces): " APP_NAME
read -p "Enter your desired resource group name (default: global-encounters-rg): " RG_NAME
RG_NAME=${RG_NAME:-global-encounters-rg}
LOCATION="eastus"

# Create resource group
echo -e "${GREEN}Creating resource group...${NC}"
az group create --name $RG_NAME --location $LOCATION

# Create Azure Container Registry
echo -e "${GREEN}Creating Azure Container Registry...${NC}"
az acr create --name $ACR_NAME --resource-group $RG_NAME --sku Basic --admin-enabled true

# Login to ACR
echo -e "${GREEN}Logging into Azure Container Registry...${NC}"
az acr login --name $ACR_NAME

# Load and tag Docker image
echo -e "${GREEN}Loading Docker image...${NC}"
docker load < global-encounters-app.tar
docker tag global-encounters-app $ACR_NAME.azurecr.io/global-encounters-app:latest

# Push to ACR
echo -e "${GREEN}Pushing image to Azure Container Registry...${NC}"
docker push $ACR_NAME.azurecr.io/global-encounters-app:latest

# Create App Service Plan
echo -e "${GREEN}Creating App Service Plan...${NC}"
az appservice plan create --name "${APP_NAME}-plan" --resource-group $RG_NAME --sku B1 --is-linux

# Create Web App
echo -e "${GREEN}Creating Web App...${NC}"
az webapp create --name $APP_NAME --resource-group $RG_NAME --plan "${APP_NAME}-plan" --deployment-container-image-name $ACR_NAME.azurecr.io/global-encounters-app:latest

# Configure environment variables
echo -e "${GREEN}Configuring environment variables...${NC}"
az webapp config appsettings set --name $APP_NAME --resource-group $RG_NAME --settings \
    DATABASE_URL="$DATABASE_URL" \
    JWT_SECRET_KEY="$JWT_SECRET_KEY" \
    PORT="8000"

# Configure container settings
echo -e "${GREEN}Configuring container settings...${NC}"
az webapp config container set --name $APP_NAME --resource-group $RG_NAME \
    --docker-custom-image-name $ACR_NAME.azurecr.io/global-encounters-app:latest \
    --docker-registry-server-url https://$ACR_NAME.azurecr.io

# Get ACR credentials
echo -e "${GREEN}Configuring ACR credentials...${NC}"
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Configure web app to use ACR
az webapp config container set --name $APP_NAME --resource-group $RG_NAME \
    --docker-registry-server-url https://$ACR_NAME.azurecr.io \
    --docker-registry-server-user $ACR_USERNAME \
    --docker-registry-server-password $ACR_PASSWORD

echo -e "${GREEN}Deployment completed!${NC}"
echo -e "Your application is available at: ${GREEN}https://$APP_NAME.azurewebsites.net${NC}"
echo -e "\nTest these endpoints:"
echo -e "1. Login: ${GREEN}https://$APP_NAME.azurewebsites.net/api/v1/login${NC}"
echo -e "2. Register: ${GREEN}https://$APP_NAME.azurewebsites.net/api/v1/register${NC}"
echo -e "3. User Search: ${GREEN}https://$APP_NAME.azurewebsites.net/api/v1/user/search${NC}"
echo -e "4. User Update: ${GREEN}https://$APP_NAME.azurewebsites.net/api/v1/user/update${NC}"

echo -e "\nTo view logs, run:"
echo -e "az webapp log tail --name $APP_NAME --resource-group $RG_NAME" 