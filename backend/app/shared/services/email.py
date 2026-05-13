"""Email service for sending notifications."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from backend.app.shared.config.email import *
from backend.app.shared.config.logger import logger

class EmailService:
    """Service for sending emails."""

    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_username = SMTP_USERNAME
        self.smtp_password = SMTP_PASSWORD
        self.smtp_use_tls = SMTP_USE_TLS
        self.from_email = FROM_EMAIL
        self.from_name = FROM_NAME

    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email to recipients."""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = ", ".join(to_emails)

            # Add text content
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)

            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)

            # Send email
            if self.smtp_username and self.smtp_password:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.smtp_use_tls:
                        server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(message)
            else:
                # For development/testing without SMTP credentials
                logger.info(f"Email would be sent to {to_emails} with subject: {subject}")

            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    async def send_welcome_email(self, email: str, full_name: str) -> bool:
        """Send welcome email to new user."""
        subject = WELCOME_EMAIL_SUBJECT
        html_content = f"""
        <html>
            <body>
                <h2>Welcome to Age Calculator, {full_name}!</h2>
                <p>Thank you for registering with our service.</p>
                <p>You can now calculate ages, view your history, and generate reports.</p>
                <p>Best regards,<br>The Age Calculator Team</p>
            </body>
        </html>
        """
        text_content = f"Welcome to Age Calculator, {full_name}! Thank you for registering."

        return await self.send_email([email], subject, html_content, text_content)

# Global email service instance
email_service = EmailService()
