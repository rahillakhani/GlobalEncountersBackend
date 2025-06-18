# Global Encounters Application Deployment Guide

## Prerequisites

1. Docker installed and running
2. PostgreSQL database running
3. Port 8000 available

## Quick Deployment

Just run the following command in the project root directory:

```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:

1. Check if Docker is running
2. Create the .env file if it doesn't exist
3. Build and run the Docker container
4. Show the deployment status

## Accessing the Application

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

If you encounter any issues:

1. Make sure Docker Desktop is running
2. Check if port 8000 is available
3. Verify PostgreSQL is running
4. Check the container logs:
   ```bash
   docker logs global-encounters
   ```

## Support

For any deployment issues, please contact the development team.
