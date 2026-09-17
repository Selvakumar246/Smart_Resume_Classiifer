# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_current_user
from app.db.database import get_db
from app.db.models import Analysis, Feedback, User
from app.schemas import UserOut

router = APIRouter(tags=["Users"])


@router.get("/users/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    analyses = db.scalars(select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).limit(10)).all()
    scores = [int((item.quality_analysis or {}).get("overall_score", 0)) for item in analyses]
    categories: dict[str, int] = {}
    for item in analyses:
        category = item.primary_role
        categories[category] = categories.get(category, 0) + 1
    return {
        "total_analyses": db.scalar(select(func.count(Analysis.id)).where(Analysis.user_id == user.id)) or 0,
        "average_ats": round(sum(scores) / len(scores)) if scores else 0,
        "top_category": max(categories, key=categories.get) if categories else "Not analyzed yet",
        "plan": user.plan,
        "recent": [
            {
                "id": item.id,
                "filename": item.resume.original_filename if item.resume else "resume",
                "category": item.primary_role,
                "ats_score": int((item.quality_analysis or {}).get("overall_score", 0)),
                "created_at": item.created_at,
            } for item in analyses[:5]
        ],
    }


@router.get("/admin/overview")
def admin_overview(_: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    analyses = db.scalars(select(Analysis)).all()
    return {
        "users": db.scalar(select(func.count(User.id))) or 0,
        "analyses": len(analyses),
        "feedback": db.scalar(select(func.count(Feedback.id))) or 0,
        "average_ats": round(sum((a.quality_analysis or {}).get("overall_score", 0) for a in analyses) / max(1, len(analyses))) if analyses else 0,
        "system_health": "healthy",
        "model": "Hybrid Semantic & Skill Overlap Classifier v1",
        "accuracy_note": "Accuracy must be measured against a labeled holdout dataset before production claims are made.",
    }
