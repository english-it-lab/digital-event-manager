from pydantic import BaseModel, EmailStr


class EmailConfirmationRequest(BaseModel):
    """Request for email confirmation code generation."""

    email: EmailStr


class EmailConfirmationResponse(BaseModel):
    """Response confirming code sent."""

    message: str
    email_masked: str


class EmailVerificationRequest(BaseModel):
    """Request for email code verification."""

    email: EmailStr
    code: str


class EmailVerificationResponse(BaseModel):
    """Response for email verification result."""

    success: bool
    message: str
