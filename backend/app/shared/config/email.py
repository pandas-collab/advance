"""Email configuration for notifications and alerts."""
import os
from typing import Dict, Any, Optional

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@agecalculator.com")
FROM_NAME = os.getenv("FROM_NAME", "Age Calculator")

def get_email_config() -> Dict[str, Any]:
    """Get email configuration."""
    return {
        "smtp_host": SMTP_HOST,
        "smtp_port": SMTP_PORT,
        "smtp_user": SMTP_USER,
        "smtp_password": SMTP_PASSWORD,
        "smtp_use_tls": SMTP_USE_TLS,
        "from_email": FROM_EMAIL,
        "from_name": FROM_NAME
    }

def validate_email_config() -> bool:
    """Validate email configuration."""
    required_fields = [SMTP_HOST, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL]
    return all(field.strip() for field in required_fields)

# Email Templates
EMAIL_TEMPLATES = {
    "api_key_created": {
        "subject": "New API Key Created - {name}",
        "template": """
        <h2>API Key Created Successfully</h2>
        <p>A new API key has been created for your account:</p>
        <ul>
            <li><strong>Name:</strong> {name}</li>
            <li><strong>Created:</strong> {created_at}</li>
            <li><strong>Rate Limit:</strong> {rate_limit} requests/hour</li>
        </ul>
        <p><strong>Important:</strong> Please store your API key securely. It will not be shown again.</p>
        """
    },
    "validation_rule_updated": {
        "subject": "Validation Rule Updated - {rule_name}",
        "template": """
        <h2>Validation Rule Updated</h2>
        <p>The validation rule "{rule_name}" has been updated.</p>
        <p><strong>Updated by:</strong> {updated_by}</p>
        <p><strong>Updated at:</strong> {updated_at}</p>
        """
    }
}
