#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting Azure Deployment...${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${RED}Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Set variables
RESOURCE_GROUP="global-encounters-rg"
LOCATION="eastus"
APP_NAME="global-encounters-app"
DB_SERVER="internal-onsite-access-dev"
DB_NAME="testdbbkup"
DB_USER="onsitedev"
DB_PASSWORD="YaRahim2025"

# Create resource group if it doesn't exist
echo -e "${GREEN}Creating resource group...${NC}"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create App Service plan
echo -e "${GREEN}Creating App Service plan...${NC}"
az appservice plan create \
    --name "${APP_NAME}-plan" \
    --resource-group $RESOURCE_GROUP \
    --sku P1v2 \
    --is-linux

# Create Web App
echo -e "${GREEN}Creating Web App...${NC}"
az webapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --plan "${APP_NAME}-plan" \
    --runtime "PYTHON|3.11"

# Configure Web App settings
echo -e "${GREEN}Configuring Web App settings...${NC}"
az webapp config appsettings set \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --settings \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true \
    ENABLE_ORYX_BUILD=true \
    PYTHON_ENABLE_VENV_CREATION=true \
    WEBSITE_RUN_FROM_PACKAGE=1 \
    DATABASE_URL="postgresql+psycopg2://${DB_USER}:${DB_PASSWORD}@${DB_SERVER}.postgres.database.azure.com:5432/${DB_NAME}?sslmode=require" \
    AZURE_POSTGRES_SSL_MODE=require \
    AZURE_POSTGRES_CONNECTION_TIMEOUT=10 \
    AZURE_POSTGRES_POOL_SIZE=20 \
    AZURE_POSTGRES_MAX_OVERFLOW=30

# Deploy the application
echo -e "${GREEN}Deploying application...${NC}"
az webapp deployment source config-local-git \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP

# Get deployment URL
DEPLOYMENT_URL=$(az webapp show --name $APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName -o tsv)

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}Your application is available at: https://${DEPLOYMENT_URL}${NC}" 