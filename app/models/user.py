from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base
import bcrypt

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "fnb"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    device_id = Column(String(100), nullable=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def verify_password(self, password_input):
        # Convert stored password from string to bytes if it's not already
        stored_password = self.password.encode('utf-8') if isinstance(self.password, str) else self.password
        # Convert input password to bytes
        input_password = password_input.encode('utf-8') if isinstance(password_input, str) else password_input
        # Compare passwords using bcrypt
        return bcrypt.checkpw(input_password, stored_password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @classmethod
    def authenticate(cls, db, login_data):
        # Try to find user by email first
        user = db.query(cls).filter(cls.email == login_data.username).first()
        # If not found by email, try to find by username
        if not user:
            user = db.query(cls).filter(cls.username == login_data.username).first()
        if not user:
            raise ValueError("User not found")
        if not user.verify_password(login_data.password):
            raise ValueError("Invalid password")
        return user 