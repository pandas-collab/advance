"""Authentication middleware for API requests."""
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..config.jwt import verify_token, decode_api_token
from ...auth.models import User, APIKey
from ..config.logger import log_security_event, log_api_request

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify JWT token
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception

        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user and verify admin privileges."""
    if not current_user.is_admin:
        log_security_event(
            "unauthorized_admin_access",
            {"user_id": current_user.user_id, "email": current_user.email},
            "WARNING"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

async def authenticate_api_key(
    x_api_key: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[Dict[str, Any]]:
    """Authenticate request via API key."""
    api_key = x_api_key or (authorization.replace("Bearer ", "") if authorization else None)

    if not api_key:
        return None

    # Hash the provided key to match stored hash
    api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # Find API key in database
    key_record = db.query(APIKey).filter(
        APIKey.api_key == api_key_hash,
        APIKey.is_active == True
    ).first()

    if not key_record:
        log_security_event(
            "invalid_api_key",
            {"provided_key_prefix": api_key[:8] + "...", "ip": "unknown"},
            "WARNING"
        )
        return None

    # Update usage statistics
    key_record.last_used = datetime.utcnow()
    key_record.usage_count += 1
    db.commit()

    # Parse permissions
    permissions = key_record.permissions.split(",") if key_record.permissions else []

    return {
        "key_id": key_record.key_id,
        "name": key_record.name,
        "permissions": permissions,
        "rate_limit": key_record.rate_limit
    }

def require_permission(permission: str):
    """Decorator to require specific permission for API key access."""
    def permission_checker(api_key_info: Dict[str, Any]) -> bool:
        if not api_key_info:
            return False
        return permission in api_key_info.get("permissions", [])

    return permission_checker

class RateLimitManager:
    """Manage rate limiting for API keys."""

    def __init__(self):
        self._usage_cache = {}  # In production, use Redis

    def check_rate_limit(self, key_id: str, rate_limit: int) -> bool:
        """Check if API key is within rate limit."""
        now = datetime.utcnow()
        hour_key = f"{key_id}:{now.hour}"

        # Get current hour usage
        current_usage = self._usage_cache.get(hour_key, 0)

        if current_usage >= rate_limit:
            log_security_event(
                "rate_limit_exceeded",
                {"key_id": key_id, "usage": current_usage, "limit": rate_limit},
                "WARNING"
            )
            return False

        # Increment usage
        self._usage_cache[hour_key] = current_usage + 1

        # Clean old entries (simple cleanup)
        keys_to_remove = [k for k in self._usage_cache.keys()
                         if k.split(":")[1] != str(now.hour)]
        for key in keys_to_remove:
            del self._usage_cache[key]

        return True

rate_limiter = RateLimitManager()
