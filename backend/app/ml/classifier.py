import json
import logging
from pathlib import Path
from app.ml.semantic_classifier import SemanticClassifier
from app.ml.skill_extractor import extract_skills_from_text
from app.services.section_detector import detect_sections

logger = logging.getLogger("smart-resume-classification")

def classify_resume(text: str, target_role: str = "", top_k: int = 5) -> list[dict]:
    """
    Main entry point for hybrid resume classification.
    Calculates weighted matches for all 18 role profiles and returns them sorted by score.
    """
    # 1. Detect sections and extract skills
    sections = detect_sections(text)
    extracted_skills_list = extract_skills_from_text(text)
    detected_skills_set = {s["canonical_name"].lower() for s in extracted_skills_list}
    
    # Get classifier instance
    classifier = SemanticClassifier.get_instance()
    profiles = classifier.profiles
    
    # 2. Get Semantic similarities (0-100)
    semantic_scores = classifier.compute_similarity(text)
    
    results = []
    
    # Lowercase sections for text matching
    exp_text = sections.get("experience", "").lower()
    proj_text = sections.get("projects", "").lower()
    
    for role_id, profile in profiles.items():
        # Component A: Semantic Similarity (40%)
        sem_score = semantic_scores.get(role_id, 0.0)
        
        # Component B: Skill Overlap (35%)
        core_skills = profile.get("core_skills", [])
        secondary_skills = profile.get("secondary_skills", [])
        
        core_matched = [s for s in core_skills if s.lower() in detected_skills_set]
        sec_matched = [s for s in secondary_skills if s.lower() in detected_skills_set]
        
        core_overlap = len(core_matched) / len(core_skills) if core_skills else 0.0
        sec_overlap = len(sec_matched) / len(secondary_skills) if secondary_skills else 0.0
        skill_score = (core_overlap * 0.7 + sec_overlap * 0.3) * 100.0
        
        # Component C: Experience Relevance (15%)
        # Look for core skills mentioned in experience text
        exp_matched_skills = [s for s in core_skills if s.lower() in exp_text]
        # Also look for role title/keywords
        role_keywords_in_exp = any(kw.lower() in exp_text for kw in profile.get("experience_keywords", []))
        
        exp_skill_ratio = len(exp_matched_skills) / len(core_skills) if core_skills else 0.0
        exp_keyword_boost = 0.2 if role_keywords_in_exp else 0.0
        exp_score = min(1.0, exp_skill_ratio + exp_keyword_boost) * 100.0
        
        # Component D: Project Relevance (10%)
        proj_matched_skills = [s for s in core_skills if s.lower() in proj_text]
        proj_skill_ratio = len(proj_matched_skills) / len(core_skills) if core_skills else 0.0
        proj_score = proj_skill_ratio * 100.0
        
        # Calculate Hybrid Score
        hybrid_score = (sem_score * 0.40) + (skill_score * 0.35) + (exp_score * 0.15) + (proj_score * 0.10)
        
        # Build evidence
        evidence = []
        # Highlight top 3 matched core skills
        if core_matched:
            evidence.append(f"Core skills detected: {', '.join(core_matched[:3])}.")
        # Highlight experience
        if exp_matched_skills:
            evidence.append(f"Experience details mention {', '.join(exp_matched_skills[:2])}.")
        elif role_keywords_in_exp:
            evidence.append(f"Work history aligns with {profile['name']} roles.")
        # Highlight projects
        if proj_matched_skills:
            evidence.append(f"Project history includes {', '.join(proj_matched_skills[:2])}.")
            
        reason = " ".join(evidence) if evidence else "Shows general semantic alignment with the role description."
        
        results.append({
            "category": profile["name"],
            "role_id": role_id,
            "confidence": round(hybrid_score, 1),
            "reason": reason,
            "evidence": core_matched + sec_matched,
            "matched_core": core_matched,
            "matched_secondary": sec_matched,
            "missing_core": [s for s in core_skills if s not in core_matched],
            "missing_secondary": [s for s in secondary_skills if s not in sec_matched]
        })
        
    # Sort by score descending
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results[:top_k]

def confidence_quality(top_results: list[dict]) -> str:
    """
    Computes classification confidence level based on score differences and evidence.
    """
    if not top_results:
        return "Low"
    top = top_results[0]["confidence"]
    margin = top - (top_results[1]["confidence"] if len(top_results) > 1 else 0.0)
    evidence_count = len(top_results[0]["evidence"])
    
    if top >= 75 and margin >= 10 and evidence_count >= 5:
        return "High"
    if top >= 50 and margin >= 5:
        return "Moderate"
    return "Low"
