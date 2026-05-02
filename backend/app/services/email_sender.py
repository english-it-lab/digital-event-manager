import logging

import aiosmtplib
from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailSenderService:
    """Service for sending emails via SMTP."""

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email
        self.use_tls = settings.smtp_use_tls

    def _is_configured(self) -> bool:
        """Checks if SMTP credentials are properly configured."""
        return bool(self.smtp_user and self.smtp_password and self.smtp_host)

    async def send_confirmation_code(self, to_email: str, code: str) -> bool:
        """
        Sends email confirmation code to the recipient.

        Args:
            to_email: Recipient email address
            code: 6-digit confirmation code

        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self._is_configured():
            logger.warning(
                "SMTP credentials not configured. "
                f"Code for {to_email}: {code} "
                "(Configure SMTP in .env to send emails)"
            )
            return False

        logger.info(
            f"Connecting to SMTP: {self.smtp_host}:{self.smtp_port}, "
            f"user={self.smtp_user}"
        )

        # Create email message
        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = "Your Confirmation Code"
        message.set_content(
            f"""
Hello,

Your confirmation code is: {code}

If you didn't request this code, please ignore this email.
"""
        )

        try:
            # Send email with timeout
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=self.use_tls,
                timeout=30,  # 30 second timeout
            )
            logger.info(f"Confirmation code sent to {to_email}")
            return True
        except aiosmtplib.SMTPTimeoutError as e:
            logger.error(f"SMTP timeout when sending to {to_email}: {e}")
            logger.error(f"SMTP host: {self.smtp_host}, port: {self.smtp_port}")
            return False
        except aiosmtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed for {to_email}: {e}")
            logger.error("Check SMTP_USER and SMTP_PASSWORD in .env")
            return False
        except aiosmtplib.SMTPException as e:
            logger.error(f"SMTP error when sending to {to_email}: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
            return False

