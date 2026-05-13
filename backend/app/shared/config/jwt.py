"""JWT token configuration and utilities."""
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise ValueError(f"Token creation failed: {e}")

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

def create_api_token(api_key_id: str, permissions: list) -> str:
    """Create API token for API key authentication."""
    data = {
        "api_key_id": api_key_id,
        "permissions": permissions,
        "type": "api_key"
    }
    # API tokens have longer expiration
    expires_delta = timedelta(hours=24)
    return create_access_token(data, expires_delta)

def decode_api_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode API token and return payload."""
    payload = verify_token(token)
    if payload and payload.get("type") == "api_key":
        return payload
    return None
