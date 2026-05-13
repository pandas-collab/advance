"""Admin panel data models."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ValidationRule(BaseModel):
    """Model for validation rules."""
    id: Optional[str] = None
    name: str
    field: str
    rule_type: str  # range, regex, custom, etc.
    parameters: Dict[str, Any]
    error_message: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ApiKey(BaseModel):
    """Model for API keys."""
    id: Optional[str] = None
    name: str
    key_preview: str
    permissions: List[str]
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_used: Optional[datetime] = None
    usage_count: int = 0

class EnterpriseConfig(BaseModel):
    """Model for enterprise configuration."""
    company_name: str
    max_calculations_per_day: int
    enable_advanced_features: bool
    custom_branding: bool
    api_rate_limit: int
    data_retention_days: int
    notification_settings: Optional[Dict[str, Any]] = None
