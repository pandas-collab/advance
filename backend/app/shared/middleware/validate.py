"""Request validation middleware and utilities."""
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException, status

class UserRegistrationRequest(BaseModel):
    """User registration validation model."""
    email: EmailStr
    password: str
    full_name: str

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('full_name')
    def validate_full_name(cls, v):
        """Validate full name."""
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        if not re.match(r'^[a-zA-Z\s\-\.]+$', v):
            raise ValueError('Full name can only contain letters, spaces, hyphens and periods')
        return v.strip()

class UserLoginRequest(BaseModel):
    """User login validation model."""
    email: EmailStr
    password: str

class CalculationRequest(BaseModel):
    """Age calculation request validation."""
    birth_date: str
    target_date: str = None
    precision_level: str = "standard"

    @validator('birth_date', 'target_date')
    def validate_dates(cls, v):
        """Validate date format."""
        if v is None:
            return v
        try:
            parsed_date = datetime.strptime(v, '%Y-%m-%d').date()
            # Check reasonable date bounds
            if parsed_date < date(1900, 1, 1):
                raise ValueError('Date cannot be before 1900')
            if parsed_date > date(2100, 12, 31):
                raise ValueError('Date cannot be after 2100')
            return v
        except ValueError as e:
            if 'does not match format' in str(e):
                raise ValueError('Date must be in YYYY-MM-DD format')
            raise e

    @validator('target_date')
    def validate_target_after_birth(cls, v, values):
        """Ensure target date is after birth date."""
        if v and 'birth_date' in values:
            birth = datetime.strptime(values['birth_date'], '%Y-%m-%d').date()
            target = datetime.strptime(v, '%Y-%m-%d').date()
            if target <= birth:
                raise ValueError('Target date must be after birth date')
        return v

    @validator('precision_level')
    def validate_precision_level(cls, v):
        """Validate precision level."""
        valid_levels = ['basic', 'standard', 'detailed', 'precise']
        if v not in valid_levels:
            raise ValueError(f'Precision level must be one of: {", ".join(valid_levels)}')
        return v

class ValidationRuleRequest(BaseModel):
    """Validation rule creation/update request."""
    name: str
    description: str = ""
    rule_config: Dict[str, Any]
    is_active: bool = True

    @validator('name')
    def validate_name(cls, v):
        """Validate rule name."""
        if len(v.strip()) < 3:
            raise ValueError('Rule name must be at least 3 characters')
        if len(v.strip()) > 100:
            raise ValueError('Rule name cannot exceed 100 characters')
        return v.strip()

    @validator('rule_config')
    def validate_rule_config(cls, v):
        """Validate rule configuration."""
        if not isinstance(v, dict):
            raise ValueError('Rule configuration must be a valid object')

        required_fields = ['type', 'parameters']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'Rule configuration must include {field}')

        valid_types = ['date_range', 'age_range', 'custom']
        if v['type'] not in valid_types:
            raise ValueError(f'Rule type must be one of: {", ".join(valid_types)}')

        return v

class APIKeyRequest(BaseModel):
    """API key creation request."""
    name: str
    permissions: List[str]
    rate_limit: int = 1000

    @validator('name')
    def validate_name(cls, v):
        """Validate API key name."""
        if len(v.strip()) < 3:
            raise ValueError('API key name must be at least 3 characters')
        if len(v.strip()) > 50:
            raise ValueError('API key name cannot exceed 50 characters')
        return v.strip()

    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions list."""
        valid_permissions = [
            'calculations.read', 'calculations.write',
            'analytics.read', 'rules.read', 'rules.write',
            'admin.read', 'admin.write'
        ]

        for perm in v:
            if perm not in valid_permissions:
                raise ValueError(f'Invalid permission: {perm}. Valid permissions: {", ".join(valid_permissions)}')

        return list(set(v))  # Remove duplicates

    @validator('rate_limit')
    def validate_rate_limit(cls, v):
        """Validate rate limit."""
        if v < 1:
            raise ValueError('Rate limit must be at least 1')
        if v > 10000:
            raise ValueError('Rate limit cannot exceed 10,000 requests per hour')
        return v

def validate_request_data(request_model: BaseModel, data: Dict[str, Any]) -> BaseModel:
    """Validate request data against model."""
    try:
        return request_model(**data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )

def sanitize_html_input(text: str) -> str:
    """Basic HTML sanitization for user inputs."""
    if not text:
        return text

    # Remove HTML tags
    import re
    clean_text = re.sub('<[^<]+?>', '', text)

    # Remove potentially dangerous characters
    clean_text = clean_text.replace('<', '&lt;').replace('>', '&gt;')

    return clean_text.strip()

class InputSanitizer:
    """Utility class for input sanitization."""

    @staticmethod
    def sanitize_string(value: str, max_length: int = 255) -> str:
        """Sanitize string input."""
        if not value:
            return ""

        # Remove null bytes and control characters
        sanitized = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')

        # Trim whitespace and limit length
        sanitized = sanitized.strip()[:max_length]

        return sanitized

    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize email input."""
        if not email:
            return ""

        # Basic email sanitization
        sanitized = email.strip().lower()

        # Remove any potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', sanitized)

        return sanitized

    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """Validate UUID format."""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))

sanitizer = InputSanitizer()
