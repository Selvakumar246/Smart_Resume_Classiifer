from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Feedback
from app.schemas import FeedbackRequest

router = APIRouter(tags=["System"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "service": "smart-resume-classification-api"}


@router.post("/feedback", status_code=201)
def create_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    item = Feedback(user_id=None, message=f"{payload.name} <{payload.email}> | {payload.subject}\n{payload.message}", rating=payload.rating)
    db.add(item)
    db.commit()
    return {"message": "Thanks. Your message has been recorded."}
