"""Authentication middleware."""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.app.shared.config.database import get_db
from backend.app.shared.config.jwt import verify_token
from backend.app.auth.service import AuthService
from backend.app.auth.models import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify token
        user_id = verify_token(credentials.credentials)
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    # Get user from database
    user = AuthService.get_user_by_id(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get current active user."""
    return current_user
