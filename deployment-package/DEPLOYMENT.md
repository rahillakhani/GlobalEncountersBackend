# Azure Deployment Instructions

## Prerequisites

1. Azure account
2. Azure CLI installed
3. Docker installed

## Step 1: Load the Docker Image

```bash
# Load the Docker image
docker load < global-encounters-app.tar
```

## Step 2: Create Azure Resources

```bash
# Login to Azure
az login

# Create a resource group
az group create --name global-encounters-rg --location eastus

# Create an Azure Container Registry (ACR)
az acr create --name yourregistryname --resource-group global-encounters-rg --sku Basic

# Login to ACR
az acr login --name yourregistryname
```

## Step 3: Push Image to Azure

```bash
# Tag the image
docker tag global-encounters-app yourregistryname.azurecr.io/global-encounters-app:latest

# Push to Azure
docker push yourregistryname.azurecr.io/global-encounters-app:latest
```

## Step 4: Create App Service

```bash
# Create App Service Plan
az appservice plan create --name global-encounters-plan --resource-group global-encounters-rg --sku B1 --is-linux

# Create Web App
az webapp create --name your-app-name --resource-group global-encounters-rg --plan global-encounters-plan --deployment-container-image-name yourregistryname.azurecr.io/global-encounters-app:latest
```

## Step 5: Configure Environment Variables

In Azure Portal:

1. Go to your App Service
2. Navigate to Configuration
3. Add these Application Settings:
   ```
   DATABASE_URL=postgresql+psycopg2://admin:admin@52.168.133.23:5432/postgres
   JWT_SECRET_KEY=your-secure-secret-key-here
   PORT=8000
   ```

## Step 6: Enable Container Registry Access

```bash
# Get ACR credentials
az acr credential show --name yourregistryname

# Configure web app to use ACR
az webapp config container set --name your-app-name --resource-group global-encounters-rg --docker-custom-image-name yourregistryname.azurecr.io/global-encounters-app:latest --docker-registry-server-url https://yourregistryname.azurecr.io
```

## Step 7: Test the Application

Your API will be available at:

```
https://your-app-name.azurewebsites.net
```

Test these endpoints:

- Login: https://your-app-name.azurewebsites.net/api/v1/login
- Register: https://your-app-name.azurewebsites.net/api/v1/register
- User Search: https://your-app-name.azurewebsites.net/api/v1/user/search
- User Update: https://your-app-name.azurewebsites.net/api/v1/user/update

## Troubleshooting

1. Check logs in Azure Portal
2. Verify environment variables
3. Ensure database is accessible from Azure
4. Check container logs: `az webapp log tail --name your-app-name --resource-group global-encounters-rg`
