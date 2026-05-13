"""Email configuration settings."""
from decouple import config

# Email settings
SMTP_HOST = config("SMTP_HOST", default="localhost")
SMTP_PORT = config("SMTP_PORT", default=587, cast=int)
SMTP_USERNAME = config("SMTP_USERNAME", default="")
SMTP_PASSWORD = config("SMTP_PASSWORD", default="")
SMTP_USE_TLS = config("SMTP_USE_TLS", default=True, cast=bool)
SMTP_USE_SSL = config("SMTP_USE_SSL", default=False, cast=bool)

FROM_EMAIL = config("FROM_EMAIL", default="noreply@agecalculator.com")
FROM_NAME = config("FROM_NAME", default="Age Calculator")

# Email templates
WELCOME_EMAIL_SUBJECT = "Welcome to Age Calculator"
PASSWORD_RESET_SUBJECT = "Password Reset Request"
