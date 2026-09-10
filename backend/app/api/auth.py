import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status

from app.auth.security import (
    create_access_token,
    create_one_time_token,
    hash_one_time_token,
    hash_password,
    verify_password,
)
from app.database.database import SessionLocal
from app.database.models import User
from app.schemas.auth import AuthRequest, AuthResponse, PasswordResetRequest, TokenRequest, UserResponse
from app.services.email_service import send_security_email
from app.config.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
async def register(data: AuthRequest):
    email = data.email.strip().lower()
    session = SessionLocal()
    try:
        if session.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=409, detail="An account with this email already exists")
        user = User(email=email, password_hash=hash_password(data.password), is_verified=not settings.REQUIRE_EMAIL_VERIFICATION)
        verification_token, user.verification_token_hash = create_one_time_token()
        session.add(user)
        session.commit()
        session.refresh(user)
        if settings.REQUIRE_EMAIL_VERIFICATION:
            await asyncio.to_thread(
                send_security_email,
                user.email,
                "Verify your WonderWise AI account",
                f"Verify your account: {settings.APP_BASE_URL}/verify-email?token={verification_token}",
            )
        return AuthResponse(
            access_token=create_access_token(user.id),
            user=UserResponse(id=user.id, email=user.email),
        )
    finally:
        session.close()


@router.post("/verify-email")
async def verify_email(data: TokenRequest):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.verification_token_hash == hash_one_time_token(data.token)).first()
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid or expired verification token")
        user.is_verified = True
        user.verification_token_hash = None
        session.commit()
        return {"status": "verified"}
    finally:
        session.close()


@router.post("/password-reset/request", status_code=202)
async def request_password_reset(data: PasswordResetRequest):
    email = data.email.strip().lower()
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user:
            token, user.reset_token_hash = create_one_time_token()
            user.reset_token_expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
            session.commit()
            await asyncio.to_thread(
                send_security_email,
                user.email,
                "Reset your WonderWise AI password",
                f"Reset your password: {settings.APP_BASE_URL}/reset-password?token={token}",
            )
    finally:
        session.close()
    return {"message": "If that email exists, reset instructions have been sent."}


@router.post("/password-reset/confirm")
async def confirm_password_reset(data: AuthRequest, token: str):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.reset_token_hash == hash_one_time_token(token)).first()
        expires_at = user.reset_token_expires_at if user else None
        if expires_at is not None and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if user is None or expires_at is None or expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")
        user.password_hash = hash_password(data.password)
        user.reset_token_hash = None
        user.reset_token_expires_at = None
        session.commit()
        return {"status": "password_reset"}
    finally:
        session.close()


@router.post("/login", response_model=AuthResponse)
async def login(data: AuthRequest):
    email = data.email.strip().lower()
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user is None or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        return AuthResponse(
            access_token=create_access_token(user.id),
            user=UserResponse(id=user.id, email=user.email),
        )
    finally:
        session.close()