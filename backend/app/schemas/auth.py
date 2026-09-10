from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenRequest(BaseModel):
    token: str = Field(..., min_length=20, max_length=256)


class PasswordResetRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)