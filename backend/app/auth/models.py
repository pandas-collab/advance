"""Database models for authentication and admin features."""
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model with admin capabilities."""
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email}, is_admin={self.is_admin})>"

class APIKey(Base):
    """API Key model for enterprise features."""
    __tablename__ = "api_keys"

    key_id = Column(String, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True, nullable=False)  # Hashed
    name = Column(String, nullable=False)
    permissions = Column(String, nullable=True)  # Comma-separated permissions
    rate_limit = Column(Integer, default=1000, nullable=False)  # Requests per hour
    created_by = Column(String, nullable=False)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_used = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<APIKey(key_id={self.key_id}, name={self.name}, rate_limit={self.rate_limit})>"

class ValidationRule(Base):
    """Validation rule model for enterprise configuration."""
    __tablename__ = "validation_rules"

    rule_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    rule_config = Column(Text, nullable=False)  # JSON configuration
    is_active = Column(Boolean, default=True, nullable=False)
    created_by = Column(String, nullable=False)  # User ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    priority = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<ValidationRule(rule_id={self.rule_id}, name={self.name}, is_active={self.is_active})>"

class CalculationHistory(Base):
    """Calculation history for analytics."""
    __tablename__ = "calculation_history"

    calculation_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True, index=True)  # Nullable for anonymous calculations
    birth_date = Column(String, nullable=False)  # Date as string
    target_date = Column(String, nullable=False)  # Date as string
    years = Column(Integer, nullable=False)
    months = Column(Integer, nullable=False)
    days = Column(Integer, nullable=False)
    total_days = Column(Integer, nullable=False)
    precision_level = Column(String, default="standard", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    api_key_id = Column(String, nullable=True, index=True)  # For API usage tracking

    def __repr__(self):
        return f"<CalculationHistory(calculation_id={self.calculation_id}, user_id={self.user_id})>"
