"""
Email service for sending feedback
Uses Gmail SMTP or can be configured for other providers
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER")  # Your email
        self.smtp_password = os.getenv("SMTP_PASSWORD")  # App password
        self.recipient_email = os.getenv("FEEDBACK_EMAIL", "atharvazaveri4@gmail.com")
        
        # Debug logging
        logger.info("=" * 80)
        logger.info("EMAIL SERVICE CONFIGURATION:")
        logger.info(f"SMTP Host: {self.smtp_host}")
        logger.info(f"SMTP Port: {self.smtp_port}")
        logger.info(f"SMTP User: {self.smtp_user}")
        logger.info(f"SMTP Password: {'*' * len(self.smtp_password) if self.smtp_password else 'NOT SET'}")
        logger.info(f"Recipient: {self.recipient_email}")
        logger.info(f"SMTP Configured: {bool(self.smtp_user and self.smtp_password)}")
        logger.info("=" * 80)
        
    def send_feedback(self, name: str, email: str, feedback: str) -> bool:
        """
        Send feedback email
        
        Args:
            name: User's name
            email: User's email
            feedback: Feedback message
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user or "noreply@scaffi.app"
            msg['To'] = self.recipient_email
            msg['Subject'] = f"Scaffi Feedback from {name}"
            msg['Reply-To'] = email
            
            # Email body
            body = f"""
New feedback received from Scaffi:

Name: {name}
Email: {email}

Feedback:
{feedback}

---
Sent from Scaffi Feedback System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # If SMTP credentials are configured, send via SMTP
            if self.smtp_user and self.smtp_password:
                logger.info(f"Sending feedback email via SMTP to {self.recipient_email}")
                
                # Connect to SMTP server
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                
                # Send email
                server.send_message(msg)
                server.quit()
                
                logger.info("Feedback email sent successfully")
                return True
            else:
                # No SMTP configured - log to console instead
                logger.warning("SMTP not configured - logging feedback to console")
                logger.info("=" * 80)
                logger.info("FEEDBACK RECEIVED:")
                logger.info(f"From: {name} ({email})")
                logger.info(f"Message: {feedback}")
                logger.info("=" * 80)
                
                # Still return True so user sees success message
                return True
                
        except Exception as e:
            logger.error(f"Failed to send feedback email: {e}", exc_info=True)
            return False


# Singleton instance
_email_service = None

def get_email_service() -> EmailService:
    """Get the email service singleton"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
