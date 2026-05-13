"""Admin panel API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.core.auth import get_current_admin_user
from app.models.admin import ValidationRule, ApiKey, EnterpriseConfig
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/config")
async def get_enterprise_config(
    admin_user=Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """Get enterprise configuration settings."""
    return await AdminService.get_enterprise_config()

@router.put("/config")
async def update_enterprise_config(
    config: EnterpriseConfig,
    admin_user=Depends(get_current_admin_user)
) -> Dict[str, Any]:
    """Update enterprise configuration settings."""
    return await AdminService.update_enterprise_config(config)

@router.get("/validation-rules")
async def get_validation_rules(
    admin_user=Depends(get_current_admin_user)
) -> List[ValidationRule]:
    """Get all validation rules."""
    return await AdminService.get_validation_rules()

@router.post("/validation-rules")
async def create_validation_rule(
    rule: ValidationRule,
    admin_user=Depends(get_current_admin_user)
) -> ValidationRule:
    """Create a new validation rule."""
    return await AdminService.create_validation_rule(rule)

@router.put("/validation-rules/{rule_id}")
async def update_validation_rule(
    rule_id: str,
    rule: ValidationRule,
    admin_user=Depends(get_current_admin_user)
) -> ValidationRule:
    """Update an existing validation rule."""
    return await AdminService.update_validation_rule(rule_id, rule)

@router.delete("/validation-rules/{rule_id}")
async def delete_validation_rule(
    rule_id: str,
    admin_user=Depends(get_current_admin_user)
) -> Dict[str, str]:
    """Delete a validation rule."""
    await AdminService.delete_validation_rule(rule_id)
    return {"message": "Validation rule deleted successfully"}

@router.get("/api-keys")
async def get_api_keys(
    admin_user=Depends(get_current_admin_user)
) -> List[ApiKey]:
    """Get all API keys."""
    return await AdminService.get_api_keys()

@router.post("/api-keys")
async def generate_api_key(
    key_data: Dict[str, Any],
    admin_user=Depends(get_current_admin_user)
) -> ApiKey:
    """Generate a new API key."""
    return await AdminService.generate_api_key(key_data)

@router.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: str,
    admin_user=Depends(get_current_admin_user)
) -> Dict[str, str]:
    """Revoke an API key."""
    await AdminService.revoke_api_key(key_id)
    return {"message": "API key revoked successfully"}
