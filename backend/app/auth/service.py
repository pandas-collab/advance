"""Authentication service logic."""
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.auth.models import User
from backend.app.shared.config.jwt import verify_password, get_password_hash, create_access_token

class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def create_user(db: Session, email: str, password: str, full_name: str) -> User:
        """Create a new user."""
        # Check if user exists
        if AuthService.get_user_by_email(db, email):
            raise ValueError("User with this email already exists")

        # Create user
        password_hash = get_password_hash(password)
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_user_token(user: User) -> str:
        """Create access token for user."""
        return create_access_token(subject=user.id)
