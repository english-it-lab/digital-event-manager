import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.adapters.api.dependencies import get_email_confirmation_service
from app.schemas.email_confirmation import (
    EmailConfirmationRequest,
    EmailConfirmationResponse,
    EmailVerificationRequest,
    EmailVerificationResponse,
)
from app.services.email_confirmation import EmailConfirmationService

router = APIRouter(tags=["email confirmation"])
logger = logging.getLogger(__name__)


@router.post(
    "/generate",
    response_model=EmailConfirmationResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_email_code(
    request: EmailConfirmationRequest,
    service: Annotated[EmailConfirmationService, Depends(get_email_confirmation_service)],
) -> EmailConfirmationResponse:
    """
    Generates and sends a 6-digit confirmation code to the email.

    The code is valid for 2-4 minutes (current and previous time window of 2 minutes each).
    """
    code, success = await service.send_code(request.email)

    if not success:
        logger.warning(f"Failed to send email to {request.email}")

    # Mask email for response (e.g., u***@example.com)
    at_index = request.email.index("@")
    email_masked = f"{request.email[:1]}***{request.email[at_index:]}"

    return EmailConfirmationResponse(
        message="Confirmation code sent to email",
        email_masked=email_masked,
    )


@router.post(
    "/verify",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_email_code(
    request: EmailVerificationRequest,
    service: Annotated[EmailConfirmationService, Depends(get_email_confirmation_service)],
) -> EmailVerificationResponse:
    """
    Verifies the confirmation code for the email.

    Returns success if the code is valid for the current or previous time window
    (code validity: 2-4 minutes depending on when it was generated).
    """
    is_valid = service.verify_code(request.email, request.code)

    if is_valid:
        return EmailVerificationResponse(
            success=True,
            message="Email verified successfully",
        )
    else:
        return EmailVerificationResponse(
            success=False,
            message="Invalid or expired code",
        )
