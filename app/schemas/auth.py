"""Pydantic schemas for authentication requests and responses."""

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Payload for creating a new user account."""

    username: str
    password: str


class LoginRequest(BaseModel):
    """Payload for authenticating an existing user."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token returned after successful registration or login."""

    access_token: str
    token_type: str = "bearer"
