import logging
from app.ml.classifier import classify_resume, confidence_quality
from app.ml.gap_analyzer import analyze_skill_gaps
from app.services.resume_quality.analyzer import run_quality_analysis
from app.ml.skill_extractor import extract_skills_from_text
from app.ml.semantic_classifier import SemanticClassifier

logger = logging.getLogger("smart-resume-classification")

def analyze_resume(text: str, target_role: str, experience_level: str, job_description: str = "") -> dict:
    """
    Unified entry point for resume analysis. Wraps the new non-fake hybrid classifier,
    gap analyzer, and quality heuristics to maintain backward compatibility.
    """
    # 1. Classify resume using hybrid classifier
    classifications = classify_resume(text, target_role)
    if not classifications:
        top_class = {"category": "Software Engineer", "confidence": 50.0, "reason": "Default classification due to lack of distinct patterns.", "role_id": "software_engineer"}
        classifications = [top_class]
    else:
        top_class = classifications[0]
        
    # 2. Extract detected skills
    detected_skills_list = extract_skills_from_text(text)
    detected_skills_names = [s["canonical_name"] for s in detected_skills_list]
    
    # 3. Analyze skill gaps
    profiles = SemanticClassifier.get_instance().profiles
    primary_role_id = top_class.get("role_id", "software_engineer")
    primary_profile = profiles.get(primary_role_id, list(profiles.values())[0])
    gaps = analyze_skill_gaps(detected_skills_names, primary_profile)
    
    # 4. Analyze quality/ATS readability
    quality = run_quality_analysis(text, target_role)
    
    # 5. Job Match / Target role comparison
    jd_match_result = None
    role_for_match = target_role.strip() if target_role.strip() else top_class["category"]
    
    # Find matching profile for match suggestion
    match_profile = next((p for p in profiles.values() if p["name"].lower() == role_for_match.lower()), primary_profile)
    matched_core = [s for s in match_profile.get("core_skills", []) if s.lower() in {x.lower() for x in detected_skills_names}]
    missing_core = [s for s in match_profile.get("core_skills", []) if s.lower() not in {x.lower() for x in detected_skills_names}]
    
    # Find score of the matched role
    matched_class = next((c for c in classifications if c["category"].lower() == role_for_match.lower()), None)
    match_score = matched_class["confidence"] if matched_class else 40.0
    
    jd_match_result = {
        "match_score": int(match_score),
        "semantic_similarity": int(match_score),
        "matched_keywords": matched_core,
        "missing_keywords": missing_core,
        "missing_soft_skills": [],
        "suggestions": [f"Add evidence for {s} through projects or work experience." for s in missing_core[:3]] or ["Your skill coverage aligns well with the target role."]
    }
        
    # Prepare top classifications format for frontend
    top_categories_list = []
    for idx, c in enumerate(classifications):
        top_categories_list.append({
            "category": c["category"],
            "confidence": c["confidence"],
            "reason": c["reason"],
            "evidence": c.get("matched_core", [])[:4]
        })
        
    return {
        "summary": {
            "word_count": len(text.split()),
            "detected_skills_count": len(detected_skills_names),
            "sections_found": sum(1 for v in quality["sections"].values() if v),
            "contact": quality["contact"]
        },
        "classification": {
            "top_categories": top_categories_list,
            "confidence_quality": confidence_quality(classifications),
            "disclaimer": "Predictions are decision support, not a hiring decision. Accuracy improves with representative labeled training data.",
            "model": "hybrid-v1",
            "validation_metrics": {}
        },
        "ats": {
            "overall_score": quality["overall_score"],
            "scores": quality["scores"],
            "deductions": quality["deductions"],
            "sections": quality["sections"]
        },
        "skills": {
            "detected": detected_skills_names,
            "gaps": gaps
        },
        "job_match": jd_match_result,
        "improvements": {
            "bullet_rewrites": quality["bullet_rewrites"],
            "action_verbs": ["achieved", "automated", "built", "created", "delivered", "designed", "developed", "drove", "implemented", "improved"],
            "recommendations": quality["top_fixes"]
        },
        "career_insights": {
            "recommended_role": top_class["category"],
            "recommended_projects": [
                f"Build a production-grade project showcasing {top_class['category']} patterns.",
                f"Create a repository focused on your core stack."
            ],
            "recommended_certifications": [
                f"Acquire a professional certification matching the {top_class['category']} track."
            ],
            "roadmap": [
                "Weeks 1–2: Target and study key technical skill gaps.",
                "Weeks 3–5: Launch a portfolio project featuring these elements.",
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
                f"What makes you a strong fit for a {top_class['category']} role?",
                "What are you hoping to achieve during your first 90 days in this position?"
            ]
        }
    }
