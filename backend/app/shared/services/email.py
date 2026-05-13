"""Email service for sending notifications and alerts."""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..config.email import get_email_config, validate_email_config, EMAIL_TEMPLATES
from ..config.logger import get_logger

logger = get_logger(__name__)
