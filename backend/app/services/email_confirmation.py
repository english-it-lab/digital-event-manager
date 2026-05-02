import hashlib
import hmac
from datetime import datetime

from app.core.config import settings
from app.services.email_sender import EmailSenderService


class EmailConfirmationService:
    """Business logic for email confirmation codes."""

    CODE_LENGTH = 6
    TIME_WINDOW_MINUTES = 2  # Time window in minutes

    def __init__(self, email_sender: EmailSenderService | None = None):
        self.email_sender = email_sender or EmailSenderService()

    def generate_code(self, email: str) -> str:
        """
        Generates a 6-digit confirmation code for the email using HMAC.

        The code is deterministic for email + timestamp (per time window),
        allowing validation within the specified period.
        """
        # Current time window (rounded to TIME_WINDOW_MINUTES)
        now = datetime.now()
        minutes = (now.hour * 60 + now.minute) // self.TIME_WINDOW_MINUTES
        time_window = f"{now.year}{now.month:02d}{now.day:02d}{minutes:05d}"

        # Create message for HMAC
        message = f"{email}:{time_window}"

        # Generate HMAC using the secret key
        hmac_hash = hmac.new(
            settings.email_confirmation_secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Convert hex hash to a number and take the last 6 digits
        code = str(int(hmac_hash, 16))[-self.CODE_LENGTH :]
        return code

    async def send_code(self, email: str) -> tuple[str, bool]:
        """
        Generates and sends confirmation code to the email.

        Args:
            email: Recipient email address

        Returns:
            Tuple of (code, success_status)
        """
        code = self.generate_code(email)
        success = await self.email_sender.send_confirmation_code(email, code)
        return code, success

    def verify_code(self, email: str, code: str) -> bool:
        """
        Verifies the correctness of the code for the email.

        Takes into account the current and previous time window
        to allow for a grace period.
        """
        # Check current window
        if self.generate_code(email) == code:
            return True

        # Check previous window (grace period)
        return self._generate_code_for_previous_window(email) == code

    def _generate_code_for_previous_window(self, email: str) -> str:
        """Generates code for the previous time window."""
        now = datetime.now()
        minutes = (now.hour * 60 + now.minute) // self.TIME_WINDOW_MINUTES
        previous_minutes = minutes - 1
        time_window = f"{now.year}{now.month:02d}{now.day:02d}{previous_minutes:05d}"

        message = f"{email}:{time_window}"

        hmac_hash = hmac.new(
            settings.email_confirmation_secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).hexdigest()

        code = str(int(hmac_hash, 16))[-self.CODE_LENGTH :]
        return code

