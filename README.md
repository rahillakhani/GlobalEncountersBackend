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
