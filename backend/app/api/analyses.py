from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import desc, select, func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import Analysis, Resume, User
from app.schemas import AnalysisDetail, AnalysisSummary
from app.services.parser import extract_resume_text
from app.ml.classifier import classify_resume, confidence_quality
from app.ml.gap_analyzer import analyze_skill_gaps
from app.services.resume_quality.analyzer import run_quality_analysis
from app.services.report import generate_pdf

router = APIRouter(prefix="/analyses", tags=["Resume analyses"])

def serialize_analysis(item: Analysis) -> dict:
    """
    Serializes a normalized database Analysis model to match the AnalysisDetail schema
    expected by the frontend React application.
    """
    filename = item.resume.original_filename if item.resume else "resume"
    raw_text = item.resume.raw_text if item.resume else ""
    
    # Structure classifications for frontend
    primary_reason = "Strong evidence from resume content."
    for alt in (item.alternative_roles or []):
        alt_category = alt.get("category") or alt.get("name")
        if alt_category == item.primary_role and "reason" in alt:
            primary_reason = alt["reason"]
            break

    top_categories = [{
        "category": item.primary_role,
        "confidence": item.primary_score,
        "reason": primary_reason,
        "evidence": item.evidence or []
    }]
    
    for alt in (item.alternative_roles or []):
        alt_category = alt.get("category") or alt.get("name")
        if alt_category and alt_category != item.primary_role:
            top_categories.append({
                "category": alt_category,
                "confidence": alt.get("confidence") or alt.get("score", 0.0),
                "reason": alt.get("reason", "Alternative alignment identified."),
                "evidence": alt.get("evidence", [])
            })
            
    # Structure career insights
    quality = item.quality_analysis or {}
    sections = item.resume_sections or {}
    gaps_formatted = []
    # Use the quality analysis skill gaps if they exist, or reconstruct them
    q_gaps = quality.get("skills", {}).get("gaps", []) if isinstance(quality.get("skills"), dict) else []
    if not q_gaps:
        # Construct them from missing_skills list
        for idx, skill in enumerate((item.missing_skills or [])[:5]):
            priority = "High" if idx < 2 else "Medium"
            difficulty = "Beginner" if skill.lower() in {"git", "sql", "linux"} else "Intermediate"
            time_est = "8–15 hours" if difficulty == "Beginner" else "20–40 hours"
            gaps_formatted.append({
                "skill": skill,
                "priority": priority,
                "difficulty": difficulty,
                "estimated_learning_time": time_est,
                "roadmap": [
                    f"Learn {skill} fundamentals",
                    f"Build a simple {skill} module",
                    f"Implement {skill} in a resume portfolio project"
                ]
            })
    else:
        gaps_formatted = q_gaps

    # Build final result dict
    quality = item.quality_analysis or {}
    sections = item.resume_sections or {}
    result_dict = {
        "summary": {
            "word_count": len(raw_text.split()),
            "detected_skills_count": len(item.detected_skills or []),
            "sections_found": sum(1 for v in sections.values() if v),
            "contact": quality.get("contact", {"emails": [], "phones": [], "github": [], "linkedin": [], "urls": []})
        },
        "classification": {
            "top_categories": top_categories,
            "confidence_quality": item.confidence or "Moderate",
            "disclaimer": "Predictions are decision support, not a hiring decision. Accuracy improves with representative labeled training data and human validation."
        },
        "ats": {
            "overall_score": quality.get("overall_score", 0),
            "scores": item.component_scores or {},
            "deductions": quality.get("deductions", []),
            "sections": sections
        },
        "skills": {
            "detected": item.detected_skills or [],
            "gaps": gaps_formatted
        },
        "job_match": None,
        "improvements": {
            "bullet_rewrites": quality.get("bullet_rewrites", []),
            "action_verbs": ["achieved", "automated", "built", "created", "delivered", "designed", "developed", "drove", "implemented", "improved", "optimized", "reduced"],
            "recommendations": quality.get("top_fixes", [])
        },
        "career_insights": {
            "recommended_role": item.primary_role,
            "recommended_projects": [
                f"Build a production-ready portfolio project featuring {item.primary_role} capabilities.",
                f"Contribute to an open-source project written with the core stack."
            ],
            "recommended_certifications": [
                f"Acquire a professional certification matching the {item.primary_role} track."
            ],
            "roadmap": [
                "Weeks 1–2: Master missing core skills.",
                "Weeks 3–5: Launch a portfolio project featuring these tools.",
                "Week 6: Align resume bullet points and apply."
            ],
            "salary_note": "Salary details are omitted pending location and experience specificity."
        },
        "interview": {
            "technical": [
                f"Explain a system you built using your core skills. What design trade-offs did you make?",
                f"How do you handle debugging and concurrency issues in your projects?"
            ],
            "project_based": [
                "Walk through your strongest project: problem statement, technical stack, your implementation, and output.",
                "What was the most challenging technical blocker you hit, and how did you resolve it?"
            ],
            "behavioral": [
                "Tell me about a time you had to pick up a new technical framework on a very tight schedule.",
                "How do you collaborate and resolve technical disagreements within a development team?"
            ],
            "hr": [
                f"What makes you a strong fit for a {item.primary_role} role?",
                "What are you hoping to achieve during your first 90 days in this position?"
            ]
        }
    }
    
    if item.target_role:
        result_dict["job_match"] = {
            "match_score": int(item.target_score or 0),
            "semantic_similarity": int(item.target_score or 0),
            "matched_keywords": item.matched_skills or [],
            "missing_keywords": item.missing_skills or [],
            "missing_soft_skills": [],
            "suggestions": [f"Highlight your experience with {skill} to improve target role alignment." for skill in (item.missing_skills or [])[:3]]
        }
        
    return {
        "id": item.id,
        "filename": filename,
        "target_role": item.target_role or "",
        "experience_level": "entry",
        "result": result_dict,
        "created_at": item.created_at
    }

def _summary(item: Analysis) -> AnalysisSummary:
    return AnalysisSummary(
        id=item.id,
        filename=item.resume.original_filename if item.resume else "resume",
        target_role=item.target_role or "",
        experience_level="entry",
        top_category=item.primary_role,
        ats_score=(item.quality_analysis or {}).get("overall_score", 0),
        created_at=item.created_at,
    )

@router.post("", response_model=AnalysisDetail, status_code=201)
async def create_analysis(
    resume: UploadFile = File(...),
    target_role: str = Form(""),
    experience_level: str = Form("entry"),
    job_description: str = Form(""),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.plan == "free":
        recent = db.scalars(select(Analysis).where(Analysis.user_id == user.id).order_by(desc(Analysis.created_at))).all()
        now = datetime.now(timezone.utc)
        monthly_count = sum(1 for item in recent if item.created_at.year == now.year and item.created_at.month == now.month)
        if monthly_count >= 3:
            raise HTTPException(status_code=402, detail="Free plan limit reached: 3 analyses per month.")

    # 1. Parse resume text
    text = await extract_resume_text(resume)
    
    # 2. Save raw Resume record
    db_resume = Resume(
        user_id=user.id,
        original_filename=resume.filename or "resume",
        file_type=Path(resume.filename or "resume").suffix.lower(),
        raw_text=text
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    # 3. Classify resume using hybrid classifier
    classifications = classify_resume(text, target_role.strip())
    if not classifications:
        raise HTTPException(status_code=422, detail="Unable to classify resume content into job roles.")
        
    top_class = classifications[0]
    
    # 4. Check target role if selected
    target_score = None
    if target_role.strip():
        matched_target = next((c for c in classifications if c["category"].lower() == target_role.strip().lower()), None)
        if matched_target:
            target_score = matched_target["confidence"]
        else:
            # Recompute to find if target_role matches out of top_k
            full_classifications = classify_resume(text, target_role=target_role.strip(), top_k=18)
            matched_target = next((c for c in full_classifications if c["category"].lower() == target_role.strip().lower()), None)
            target_score = matched_target["confidence"] if matched_target else 0.0

    # 5. Extract skills for gap analysis
    from app.ml.skill_extractor import extract_skills_from_text
    detected_skills_list = extract_skills_from_text(text)
    detected_skills_names = [s["canonical_name"] for s in detected_skills_list]
    
    # Load primary matched role profile
    from app.ml.semantic_classifier import SemanticClassifier
    profiles = SemanticClassifier.get_instance().profiles
    
    primary_role_id = top_class.get("role_id", "software_engineer")
    primary_profile = profiles.get(primary_role_id, list(profiles.values())[0])
    
    # Skill matches & gaps
    matched_skills = [s for s in primary_profile.get("core_skills", []) if s.lower() in {x.lower() for x in detected_skills_names}]
    missing_skills = [s for s in primary_profile.get("core_skills", []) if s.lower() not in {x.lower() for x in detected_skills_names}]
    
    # 6. Run Quality Analysis
    quality_result = run_quality_analysis(text, target_role=target_role.strip())
    
    # Map alternative roles
    alt_roles = [
        {
            "category": c["category"],
            "name": c["category"],
            "confidence": c["confidence"],
            "score": c["confidence"],
            "reason": c.get("reason", "Alternative alignment identified."),
            "evidence": c.get("evidence", [])
        }
        for c in classifications
    ]
    
    # Categories mapping of detected skills
    skill_cats = {}
    for s in detected_skills_list:
        cat = s["category"]
        skill_cats[cat] = skill_cats.get(cat, []) + [s["canonical_name"]]

    # 7. Create Analysis database record
    analysis = Analysis(
        resume_id=db_resume.id,
        user_id=user.id,
        primary_role=top_class["category"],
        primary_score=top_class["confidence"],
        confidence=confidence_quality(classifications),
        target_role=target_role.strip() if target_role.strip() else None,
        target_score=target_score,
        classifier_version="hybrid-v1",
        alternative_roles=alt_roles,
        detected_skills=detected_skills_names,
        skill_categories=skill_cats,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        evidence=top_class.get("matched_core", []) + top_class.get("matched_secondary", []),
        quality_analysis=quality_result,
        component_scores=quality_result["scores"],
        resume_sections=quality_result["sections"]
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    # 8. Return formatted detail payload
    serialized = serialize_analysis(analysis)
    return AnalysisDetail(**serialized)

@router.get("", response_model=list[AnalysisSummary])
def list_analyses(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.scalars(select(Analysis).where(Analysis.user_id == user.id).order_by(desc(Analysis.created_at)).limit(50)).all()
    return [_summary(item) for item in items]

@router.get("/{analysis_id}", response_model=AnalysisDetail)
def get_analysis(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Analysis).where(Analysis.id == analysis_id))
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    serialized = serialize_analysis(item)
    return AnalysisDetail(**serialized)

@router.delete("/{analysis_id}", status_code=204)
def delete_analysis(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Analysis).where(Analysis.id == analysis_id))
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    db.delete(item)
    db.commit()

@router.get("/{analysis_id}/report")
def download_report(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.scalar(select(Analysis).where(Analysis.id == analysis_id))
    if not item or item.user_id != user.id:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    serialized = serialize_analysis(item)
    path = generate_pdf(item.id, serialized["filename"], serialized["result"])
    return FileResponse(path, media_type="application/pdf", filename=path.name)
