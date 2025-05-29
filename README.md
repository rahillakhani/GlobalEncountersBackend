# Global Encounters Application Backend

## Deployment Instructions

### Prerequisites

- Docker installed on the server
- PostgreSQL database
- Environment variables configured

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# REQUIRED: Database connection string
DATABASE_URL=postgresql+psycopg2://username:password@host:5432/database_name

# REQUIRED: Secret key for JWT token generation and verification
JWT_SECRET_KEY=your-secure-secret-key-here

# OPTIONAL: Port number (defaults to 8000 if not set)
PORT=8000
```

Note: Both DATABASE_URL and JWT_SECRET_KEY are required for the application to function. The PORT variable is optional.

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

- Login: `/api/v1/login`
- Register: `/api/v1/register`
- User Search: `/api/v1/user/search`
- User Update: `/api/v1/user/update`
- User Profile: `/api/v1/users/me`

### Security Notes

1. Make sure to use a strong JWT_SECRET_KEY
2. Keep your database credentials secure
3. In production, update the CORS settings in main.py to allow only your frontend domain

### Troubleshooting

If you encounter any issues:

1. Check the container logs: `docker logs global-encounters`
2. Verify environment variables are set correctly
3. Ensure database is accessible from the container
# GlobalEncountersBackend
