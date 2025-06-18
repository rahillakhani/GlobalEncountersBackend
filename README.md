[![Build and deploy Python app to Azure Web App - fnb-gef2025-dev](https://github.com/rahillakhani/GlobalEncountersBackend/actions/workflows/main_fnb-gef2025-dev.yml/badge.svg)](https://github.com/rahillakhani/GlobalEncountersBackend/actions/workflows/main_fnb-gef2025-dev.yml)

# Global Encounters Application Backend

## Deployment Instructions

### Prerequisites

- Docker installed on the server
- PostgreSQL database
- Environment variables configured

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=global_encounters

# Application Configuration
PORT=8000
```

### Database Setup

1. Create a PostgreSQL database:

```bash
createdb global_encounters
```

2. Run database migrations:

```bash
alembic upgrade head
```

### Building and Running with Docker

1. Build the Docker image:

```bash
docker build -t global-encounters-app .
```

2. Run the container:

```bash
docker run -d \
  --name global-encounters \
  -p 8000:8000 \
  --env-file .env \
  global-encounters-app
```

### API Endpoints

The application will be available at:

- Local: http://localhost:8000
- Azure: https://your-app-name.azurewebsites.net

Main endpoints:

- User Search: `/api/v1/user/search`
- User Update: `/api/v1/user/update`
- User Profile: `/api/v1/users/me`

### Security Notes

1. Keep your database credentials secure
2. In production, update the CORS settings in main.py to allow only your frontend domain
3. Use strong passwords for your PostgreSQL database
4. Consider using SSL for database connections in production

### Troubleshooting

If you encounter any issues:

1. Check the container logs: `docker logs global-encounters`
2. Verify environment variables are set correctly
3. Ensure database is accessible from the container
4. Check database connection: `psql -h localhost -U postgres -d global_encounters`

## Azure Deployment

### Prerequisites

1. Azure CLI installed
2. Azure account with appropriate permissions
3. Git installed

### Deployment Steps

1. **Login to Azure**

   ```bash
   az login
   ```

2. **Make the deployment script executable**

   ```bash
   chmod +x azure-deploy.sh
   ```

3. **Run the deployment script**

   ```bash
   ./azure-deploy.sh
   ```

4. **Configure GitHub Actions (Optional)**
   - Go to your GitHub repository settings
   - Add the following secrets:
     - `AZURE_WEBAPP_PUBLISH_PROFILE`: Your Azure Web App publish profile
   - Push to main branch to trigger deployment

### Manual Deployment

1. **Create Azure resources**

   ```bash
   az group create --name global-encounters-rg --location eastus
   az appservice plan create --name global-encounters-plan --resource-group global-encounters-rg --sku P1v2 --is-linux
   az webapp create --name global-encounters-app --resource-group global-encounters-rg --plan global-encounters-plan --runtime "PYTHON|3.11"
   ```

2. **Configure environment variables**

   ```bash
   az webapp config appsettings set --name global-encounters-app --resource-group global-encounters-rg --settings @azure-app-service.yaml
   ```

3. **Deploy the application**
   ```bash
   az webapp deployment source config-local-git --name global-encounters-app --resource-group global-encounters-rg
   git remote add azure <deployment-url>
   git push azure main
   ```

### Monitoring and Logs

1. **View application logs**

   ```bash
   az webapp log tail --name global-encounters-app --resource-group global-encounters-rg
   ```

2. **Monitor application metrics**
   - Go to Azure Portal
   - Navigate to your Web App
   - Click on "Metrics" in the left menu

### Troubleshooting

1. **Check application logs**

   ```bash
   az webapp log download --name global-encounters-app --resource-group global-encounters-rg
   ```

2. **Restart the application**

   ```bash
   az webapp restart --name global-encounters-app --resource-group global-encounters-rg
   ```

3. **Check application status**
   ```bash
   az webapp show --name global-encounters-app --resource-group global-encounters-rg
   ```
