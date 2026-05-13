"""Authentication related database models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from backend.app.shared.config.database import Base

class User(Base):
    """User model for authentication."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Calculation(Base):
    """Model for storing calculation history."""
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=True)  # NULL for anonymous calculations
    birth_date = Column(String(50), nullable=False)
    target_date = Column(String(50), nullable=False)
    timezone = Column(String(100), default="UTC")
    result_data = Column(Text)  # JSON string of calculation results
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class APIKey(Base):
    """Model for API key management."""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    key_name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False)
    permissions = Column(Text)  # JSON string of permissions
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ValidationRule(Base):
    """Model for business validation rules."""
    __tablename__ = "validation_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rule_name = Column(String(255), unique=True, nullable=False)
    rule_type = Column(String(100), nullable=False)  # date_range, age_limit, etc.
    rule_config = Column(Text)  # JSON configuration
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
