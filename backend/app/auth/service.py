"""Authentication and authorization service with admin capabilities."""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid
import secrets
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .models import User, APIKey, ValidationRule
from ..shared.config.jwt import create_access_token, verify_token
from ..shared.config.database import get_db_session
from ..core.security import verify_password, get_password_hash

class AuthService:
    """Service for authentication and admin operations."""

    def __init__(self):
        pass

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        try:
            with get_db_session() as db:
                user = db.query(User).filter(User.email == email).first()
                if user and verify_password(password, user.password_hash):
                    return user
                return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None

    def create_user(self, email: str, password: str, full_name: str, is_admin: bool = False) -> Optional[User]:
        """Create new user account."""
        try:
            with get_db_session() as db:
                # Check if user already exists
                existing_user = db.query(User).filter(User.email == email).first()
                if existing_user:
                    return None

                user = User(
                    user_id=str(uuid.uuid4()),
                    email=email,
                    password_hash=get_password_hash(password),
                    full_name=full_name,
                    is_admin=is_admin,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
        except Exception as e:
            print(f"User creation error: {e}")
            return None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            with get_db_session() as db:
                return db.query(User).filter(User.user_id == user_id).first()
        except Exception as e:
            print(f"User lookup error: {e}")
            return None

    # Admin API Key Management
    def create_api_key(self, name: str, permissions: List[str], rate_limit: int, user_id: str) -> Optional[Dict[str, Any]]:
        """Create new API key with specified permissions and rate limits."""
        try:
            with get_db_session() as db:
                # Generate secure API key
                api_key = f"ak_{secrets.token_urlsafe(32)}"
                key_id = str(uuid.uuid4())

                api_key_obj = APIKey(
                    key_id=key_id,
                    api_key=hashlib.sha256(api_key.encode()).hexdigest(),
                    name=name,
                    permissions=",".join(permissions),
                    rate_limit=rate_limit,
                    created_by=user_id,
                    created_at=datetime.utcnow(),
                    is_active=True
                )
                db.add(api_key_obj)
                db.commit()

                return {
                    "api_key_id": key_id,
                    "api_key": api_key,  # Return plain key only once
                    "name": name,
                    "permissions": permissions,
                    "rate_limit": rate_limit
                }
        except Exception as e:
            print(f"API key creation error: {e}")
            return None

    def get_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all API keys created by user."""
        try:
            with get_db_session() as db:
                keys = db.query(APIKey).filter(
                    and_(APIKey.created_by == user_id, APIKey.is_active == True)
                ).all()

                return [{
                    "key_id": key.key_id,
                    "name": key.name,
                    "permissions": key.permissions.split(",") if key.permissions else [],
                    "rate_limit": key.rate_limit,
                    "created_at": key.created_at.isoformat(),
                    "last_used": key.last_used.isoformat() if key.last_used else None
                } for key in keys]
        except Exception as e:
            print(f"API key retrieval error: {e}")
            return []

    def revoke_api_key(self, key_id: str, user_id: str) -> bool:
        """Revoke API key."""
        try:
            with get_db_session() as db:
                key = db.query(APIKey).filter(
                    and_(APIKey.key_id == key_id, APIKey.created_by == user_id)
                ).first()

                if key:
                    key.is_active = False
                    key.updated_at = datetime.utcnow()
                    db.commit()
                    return True
                return False
        except Exception as e:
            print(f"API key revocation error: {e}")
            return False

    # Validation Rule Management
    def create_validation_rule(self, name: str, description: str, rule_config: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
        """Create new validation rule."""
        try:
            with get_db_session() as db:
                rule_id = str(uuid.uuid4())

                rule = ValidationRule(
                    rule_id=rule_id,
                    name=name,
                    description=description,
                    rule_config=str(rule_config),  # Store as JSON string
                    is_active=True,
                    created_by=user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(rule)
                db.commit()

                return {
                    "rule_id": rule_id,
                    "name": name,
                    "description": description,
                    "is_active": True
                }
        except Exception as e:
            print(f"Validation rule creation error: {e}")
            return None

    def get_validation_rules(self) -> List[Dict[str, Any]]:
        """Get all validation rules."""
        try:
            with get_db_session() as db:
                rules = db.query(ValidationRule).filter(ValidationRule.is_active == True).all()

                return [{
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "description": rule.description,
                    "is_active": rule.is_active,
                    "created_at": rule.created_at.isoformat()
                } for rule in rules]
        except Exception as e:
            print(f"Validation rule retrieval error: {e}")
            return []

    def update_validation_rule(self, rule_id: str, **kwargs) -> bool:
        """Update validation rule."""
        try:
            with get_db_session() as db:
                rule = db.query(ValidationRule).filter(ValidationRule.rule_id == rule_id).first()
                if rule:
                    for key, value in kwargs.items():
                        if hasattr(rule, key):
                            setattr(rule, key, value)
                    rule.updated_at = datetime.utcnow()
                    db.commit()
                    return True
                return False
        except Exception as e:
            print(f"Validation rule update error: {e}")
            return False

    # Admin Analytics
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get system usage analytics."""
        try:
            with get_db_session() as db:
                # Mock analytics data - in real implementation would query actual data
                return {
                    "total_calculations": 1250,
                    "active_users": 45,
                    "api_usage": {
                        "total_requests": 15600,
                        "requests_today": 340,
                        "avg_response_time": "125ms"
                    },
                    "system_metrics": {
                        "cpu_usage": "23%",
                        "memory_usage": "45%",
                        "disk_usage": "12%",
                        "uptime": "7d 4h 23m"
                    }
                }
        except Exception as e:
            print(f"Analytics retrieval error: {e}")
            return {}

# Global service instance
auth_service = AuthService()
