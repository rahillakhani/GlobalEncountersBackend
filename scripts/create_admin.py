from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.user import User

def create_admin_user():
    # Create database engine
    engine = create_engine(settings.get_database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if admin user already exists
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            print("Admin user already exists")
            return

        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw("admin".encode('utf-8'), salt)

        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password=hashed_password.decode('utf-8')
        )

        db.add(admin_user)
        db.commit()
        print("Admin user created successfully")
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 