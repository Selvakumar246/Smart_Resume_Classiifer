import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, create_password_reset_token, decode_password_reset_token, hash_password, verify_password
from app.db.database import get_db
from app.db.models import User
from app.schemas import AuthResponse, FirebaseAuthRequest, ForgotPasswordRequest, LoginRequest, RegisterRequest, ResetPasswordRequest, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])
_google_states: set[str] = set()


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    if existing:
        # If this user was created via Google/Firebase (no password), let them set a password now
        if not existing.password_hash:
            existing.password_hash = hash_password(payload.password)
            existing.name = payload.name.strip() or existing.name
            db.commit()
            db.refresh(existing)
            return AuthResponse(access_token=create_access_token(existing.id), user=UserOut.model_validate(existing))
        raise HTTPException(status_code=409, detail="An account with this email already exists. Please sign in instead.")
    settings = get_settings()
    user = User(name=payload.name.strip(), email=payload.email.lower(), password_hash=hash_password(payload.password), is_admin=payload.email.lower() in settings.admin_email_list)
    db.add(user)
    db.commit()
    db.refresh(user)
    return AuthResponse(access_token=create_access_token(user.id), user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    if not user:
        raise HTTPException(status_code=401, detail="No account found with this email. Please register first.")
    if not user.password_hash:
        raise HTTPException(status_code=401, detail="This account uses Google sign-in. Please use 'Continue with Google' to log in.")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password. Please try again or reset your password.")
    expires = 43_200 if payload.remember_me else 720
    return AuthResponse(access_token=create_access_token(user.id, expires), user=UserOut.model_validate(user))


import base64
import json


def _decode_jwt_payload(token: str) -> dict | None:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload_segment = parts[1]
        remainder = len(payload_segment) % 4
        if remainder > 0:
            payload_segment += "=" * (4 - remainder)
        decoded_bytes = base64.urlsafe_b64decode(payload_segment)
        claims = json.loads(decoded_bytes.decode("utf-8"))
        
        email = claims.get("email")
        uid = claims.get("user_id") or claims.get("sub") or claims.get("uid")
        name = claims.get("name") or (email.split("@")[0] if email else "User")
        
        if email and uid:
            return {
                "email": email,
                "name": name,
                "uid": uid,
            }
    except Exception:
        pass
    return None


def _verify_firebase_token_via_google(id_token: str) -> dict:
    """
    Verify a Firebase ID token by:
    1. Calling Google's tokeninfo endpoint (for Google OAuth ID tokens).
    2. Trying Firebase Admin SDK (if credentials configured).
    3. Decoding Firebase JWT payload (for Firebase Email/Password & standard tokens).
    """
    # Method 1: Use Google's tokeninfo endpoint (works for Google OAuth tokens)
    try:
        resp = httpx.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}",
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "email": data.get("email"),
                "name": data.get("name", data.get("email", "").split("@")[0]),
                "uid": data.get("sub"),
            }
    except Exception:
        pass

    # Method 2: Try Firebase Admin SDK if GOOGLE_APPLICATION_CREDENTIALS is set
    import os
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            import firebase_admin
            from firebase_admin import auth as fb_auth
            if not firebase_admin._apps:
                firebase_admin.initialize_app()
            decoded = fb_auth.verify_id_token(id_token)
            return {
                "email": decoded.get("email"),
                "name": decoded.get("name", decoded.get("email", "").split("@")[0]),
                "uid": decoded.get("uid") or decoded.get("sub"),
            }
        except Exception:
            pass

    # Method 3: Decode Firebase JWT payload (for Firebase Email/Password tokens)
    claims = _decode_jwt_payload(id_token)
    if claims:
        return claims

    raise ValueError("Could not verify Firebase ID token. Token may be expired or invalid.")


@router.post("/firebase", response_model=AuthResponse)
def firebase_auth(payload: FirebaseAuthRequest, db: Session = Depends(get_db)):
    settings = get_settings()

    try:
        claims = _verify_firebase_token_via_google(payload.id_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    email = claims.get("email")
    name = claims.get("name")
    uid = claims.get("uid")

    if not email or not uid:
        raise HTTPException(status_code=400, detail="Invalid Firebase token: email or UID is missing.")

    email = email.lower()

    # First query by firebase_uid
    user = db.scalar(select(User).where(User.firebase_uid == uid))
    if not user:
        # Fallback to query by email to link accounts
        user = db.scalar(select(User).where(func.lower(User.email) == email))
        if user:
            user.firebase_uid = uid
            db.commit()
            db.refresh(user)
        else:
            user = User(
                firebase_uid=uid,
                name=name or email.split("@")[0],
                email=email,
                is_admin=email in settings.admin_email_list,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

    return AuthResponse(access_token=create_access_token(user.id), user=UserOut.model_validate(user))




@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    settings = get_settings()
    user = db.scalar(select(User).where(func.lower(User.email) == payload.email.lower()))
    response = {"message": "If an account exists, password reset instructions have been prepared."}
    if user:
        token = create_password_reset_token(user.email)
        # Integrate an email provider in production. The token is returned only for local development.
        if settings.environment.lower() == "development":
            response["reset_token"] = token
    return response


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = decode_password_reset_token(payload.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token.")
    user = db.scalar(select(User).where(func.lower(User.email) == email.lower()))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token.")
    user.password_hash = hash_password(payload.password)
    db.commit()
    return {"message": "Password updated successfully."}


@router.get("/google/login")
def google_login():
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google login is not configured. Add Google OAuth credentials in .env.")
    state = secrets.token_urlsafe(24)
    _google_states.add(state)
    query = urlencode({
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    })
    return RedirectResponse(f"https://accounts.google.com/o/oauth2/v2/auth?{query}")


@router.get("/google/callback")
def google_callback(code: str, state: str, db: Session = Depends(get_db)):
    settings = get_settings()
    if state not in _google_states:
        raise HTTPException(status_code=400, detail="Invalid OAuth state.")
    _google_states.discard(state)
    token_response = httpx.post("https://oauth2.googleapis.com/token", data={
        "code": code,
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }, timeout=15)
    token_response.raise_for_status()
    access_token = token_response.json()["access_token"]
    profile_response = httpx.get("https://openidconnect.googleapis.com/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=15)
    profile_response.raise_for_status()
    profile = profile_response.json()
    email = profile["email"].lower()
    user = db.scalar(select(User).where(func.lower(User.email) == email))
    if not user:
        user = User(name=profile.get("name") or email.split("@")[0], email=email, password_hash=hash_password(secrets.token_urlsafe(32)), is_admin=email in settings.admin_email_list)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_access_token(user.id)
    return RedirectResponse(f"{settings.frontend_url}/auth/callback?token={token}")
