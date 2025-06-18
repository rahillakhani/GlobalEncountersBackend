from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# Create engine with connection pooling and timeout settings optimized for Azure PostgreSQL
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=20,  # Increased pool size for better performance
    max_overflow=30,  # Increased max overflow for handling more concurrent connections
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection from the pool
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=1800,  # Recycle connections after 30 minutes
    connect_args={
        "connect_timeout": 10,  # Seconds to wait for establishing a connection
        "keepalives": 1,  # Enable TCP keepalive
        "keepalives_idle": 30,  # Seconds between TCP keepalive probes
        "keepalives_interval": 10,  # Seconds between TCP keepalive retransmits
        "keepalives_count": 5,  # Number of TCP keepalive retransmits
        "sslmode": "require"  # Require SSL for Azure PostgreSQL
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 