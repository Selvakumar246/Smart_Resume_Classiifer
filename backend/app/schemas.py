from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class FirebaseAuthRequest(BaseModel):
    id_token: str



class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    plan: str
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class AnalysisSummary(BaseModel):
    id: str
    filename: str
    target_role: str
    experience_level: str
    top_category: str
    ats_score: int
    created_at: datetime


class AnalysisDetail(BaseModel):
    id: str
    filename: str
    target_role: str
    experience_level: str
    result: dict[str, Any]
    created_at: datetime


class FeedbackRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=160)
    message: str = Field(min_length=5, max_length=2000)
    rating: int = Field(default=5, ge=1, le=5)
