# Azure Deployment Guide

## Package Contents

1. `.env` - Environment configuration file
2. `azure-deploy.yaml` - GitHub Actions workflow file
3. `azure-app-service.yaml` - Azure App Service configuration
4. `azure-deploy.sh` - Deployment script
5. `README.md` - Project documentation

## Prerequisites

1. Azure CLI installed
2. Azure account with appropriate permissions
3. Git installed

## Deployment Steps

### Option 1: Automated Deployment (Recommended)

1. **Set up GitHub Repository**

   - Push the code to your GitHub repository
   - Go to repository settings
   - Add the following secret:
     - `AZURE_WEBAPP_PUBLISH_PROFILE`: Your Azure Web App publish profile

2. **Deploy**
   - Push to main branch to trigger deployment
   - Or manually trigger the workflow from GitHub Actions

### Option 2: Manual Deployment

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

## Configuration

### Environment Variables

The `.env` file contains all necessary configuration:

- Database connection string
- JWT settings
- Application settings
- Azure PostgreSQL settings
- Security settings

### Database Configuration

- Server: internal-onsite-access-dev.postgres.database.azure.com
- Database: testdbbkup
- Username: onsitedev
- Password: YaRahim2025

## Monitoring

1. **View application logs**

   ```bash
   az webapp log tail --name global-encounters-app --resource-group global-encounters-rg
   ```

2. **Monitor application metrics**
   - Go to Azure Portal
   - Navigate to your Web App
   - Click on "Metrics" in the left menu

## Troubleshooting

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

## Support

For any deployment issues, please contact the development team.
