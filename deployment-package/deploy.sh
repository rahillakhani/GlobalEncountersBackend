#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Starting Global Encounters App Deployment...${NC}"

if ! command -v docker &> /dev/null; then
  echo -e "${RED}Docker is not installed. Please install it first.${NC}"
  echo "Visit: https://docs.docker.com/get-docker/"
  exit 1
fi

if [ -f .env ]; then
  source .env
else
  echo -e "${RED}No .env file found. Creating one...${NC}"
  cat > .env << EOL
DATABASE_URL=postgresql+psycopg2://admin:admin@localhost:5432/postgres
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_REFRESH_SECRET_KEY=$(openssl rand -hex 32)
PORT=8000
EOL
  echo -e "${GREEN}Created .env file with default values${NC}"
fi

IMAGE_NAME="global-encounters-app"
TAR_FILE="${IMAGE_NAME}.tar"
SOURCE_PATH=".."
DOCKERFILE_PATH="../Dockerfile"

echo -e "${GREEN}Building Docker image...${NC}"
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH $SOURCE_PATH

echo -e "${GREEN}Saving Docker image to tar file...${NC}"
docker save $IMAGE_NAME -o $TAR_FILE

echo -e "${GREEN}Loading Docker image from tar file...${NC}"
docker load < $TAR_FILE

docker rm -f $IMAGE_NAME 2>/dev/null

NETWORK_NAME="festival-access-control_app-net"
POSTGRES_CONTAINER_NAME="festival-acl-db"

if docker network ls --format '{{.Name}}' | grep -q "^${NETWORK_NAME}$"; then
  echo -e "${GREEN}Docker network '${NETWORK_NAME}' found.${NC}"
  DB_HOST=$POSTGRES_CONTAINER_NAME
else
  echo -e "${RED}Docker network '${NETWORK_NAME}' not found.${NC}"
  DB_HOST=localhost
fi

sed -i.bak "s|DATABASE_URL=.*|DATABASE_URL=postgresql+psycopg2://admin:admin@$DB_HOST:5432/postgres|" .env

docker rm -f $IMAGE_NAME 2>/dev/null

if [ "$DB_HOST" = "$POSTGRES_CONTAINER_NAME" ]; then
  docker run -d -p 8000:8000 --name $IMAGE_NAME --network $NETWORK_NAME --env-file .env $IMAGE_NAME
else
  docker run -d -p 8000:8000 --name $IMAGE_NAME --env-file .env $IMAGE_NAME
fi

read -p "Do you want to deploy to Azure App Service? (y/n): " DEPLOY_AZURE

if [[ "$DEPLOY_AZURE" == "y" || "$DEPLOY_AZURE" == "Y" ]]; then
  read -p "Enter your desired Azure Container Registry name (lowercase, no spaces): " ACR_NAME
  read -p "Enter your desired App Service name (lowercase, no spaces): " APP_NAME
  read -p "Enter your desired resource group name (default: global-encounters-rg): " RG_NAME
  RG_NAME=${RG_NAME:-global-encounters-rg}
  LOCATION="eastus"

  echo -e "${GREEN}Logging into Azure Container Registry...${NC}"
  az acr login --name $ACR_NAME

  docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

  echo -e "${GREEN}Pushing image to Azure Container Registry...${NC}"
  docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

  echo -e "${GREEN}Creating resource group...${NC}"
  az group create --name $RG_NAME --location $LOCATION

  echo -e "${GREEN}Creating Azure Container Registry...${NC}"
  az acr create --name $ACR_NAME --resource-group $RG_NAME --sku Basic --admin-enabled true

  echo -e "${GREEN}Creating App Service Plan...${NC}"
  az appservice plan create --name "${APP_NAME}-plan" --resource-group $RG_NAME --sku B1 --is-linux

  echo -e "${GREEN}Creating Web App...${NC}"
  az webapp create --name $APP_NAME --resource-group $RG_NAME --plan "${APP_NAME}-plan" --deployment-container-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

  echo -e "${GREEN}Configuring environment variables...${NC}"
  az webapp config appsettings set --name $APP_NAME --resource-group $RG_NAME --settings DATABASE_URL="$DATABASE_URL" JWT_SECRET_KEY="$JWT_SECRET_KEY" JWT_REFRESH_SECRET_KEY="$JWT_REFRESH_SECRET_KEY" PORT="8000"

  echo -e "${GREEN}Configuring container settings...${NC}"
  az webapp config container set --name $APP_NAME --resource-group $RG_NAME --docker-custom-image-name $ACR_NAME.azurecr.io/$IMAGE_NAME:latest --docker-registry-server-url https://$ACR_NAME.azurecr.io

  echo -e "${GREEN}Configuring ACR credentials...${NC}"
  ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
  ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

  az webapp config container set --name $APP_NAME --resource-group $RG_NAME --docker-registry-server-user $ACR_USERNAME --docker-registry-server-password $ACR_PASSWORD

  echo -e "${GREEN}Deployment completed!${NC}"
  echo -e "Your application is available at: ${GREEN}https://$APP_NAME.azurewebsites.net${NC}"
else
  echo -e "${GREEN}Docker deployment completed without Azure App Service deployment.${NC}"
fi
