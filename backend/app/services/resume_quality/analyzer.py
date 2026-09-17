import logging
from app.services.section_detector import detect_sections
from app.ml.skill_extractor import extract_skills_from_text

# Import sub-analyzers
from app.services.resume_quality.scoring import calculate_quality_score
from app.services.resume_quality.section_analyzer import analyze_sections
from app.services.resume_quality.experience_analyzer import analyze_experience
from app.services.resume_quality.project_analyzer import analyze_projects
from app.services.resume_quality.language_analyzer import analyze_language
from app.services.resume_quality.consistency_analyzer import analyze_consistency
from app.services.resume_quality.ats_analyzer import analyze_ats_readability
from app.services.resume_quality.contact_analyzer import analyze_contact_info

logger = logging.getLogger("smart-resume-classification")

def analyze_skill_evidence(detected_skills: list[str], sections: dict[str, str]) -> tuple[int, list[dict]]:
    """
    Checks if skills listed in the skills section have supporting evidence in Experience or Projects.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    
    exp_and_proj_text = (sections.get("experience", "") + " " + sections.get("projects", "")).lower()
    
    unsupported = []
    for skill in detected_skills:
        if skill.lower() not in exp_and_proj_text:
            unsupported.append(skill)
            
    if unsupported:
        # Penalize score based on proportion of unsupported skills
        penalty = min(25, len(unsupported) * 4)
        score -= penalty
        
        # Group them to avoid listing 20 separate issues
        issues.append({
            "category": "Skill Evidence",
            "severity": "important",
            "title": "Skills listed without supporting context",
            "evidence": f"No project or experience context found for: {', '.join(unsupported[:5])}.",
            "recommendation": "Technical skills like " + ", ".join(unsupported[:3]) + " are listed in your skills section but lack matching mentions in your work history or projects. Integrate these keywords into descriptions to show context."
        })
        
    return max(0, score), issues

def run_quality_analysis(text: str, target_role: str = "") -> dict:
    """
    Orchestrates the resume quality analysis process.
    Returns a unified dict containing scores, deductions/issues, and structural information.
    """
    # 1. Segment the resume
    sections = detect_sections(text)
    
    # Count how many sections were successfully identified (non-empty)
    sections_found_count = sum(1 for sec, content in sections.items() if content.strip())
    
    # 2. Extract skills
    extracted_skills_list = extract_skills_from_text(text)
    detected_skills = [s["canonical_name"] for s in extracted_skills_list]
    
    # 3. Run individual checks
    structure_score, structure_issues = analyze_sections(sections)
    contact_score, contact_issues, parsed_contact = analyze_contact_info(text)
    
    # Evaluate summary (if summary section is present)
    summary_text = sections.get("summary", "")
    from app.services.resume_quality.summary_analyzer import analyze_summary
    summary_score, summary_issues = analyze_summary(summary_text, target_role)
    
    # Evaluate experience bullets
    exp_text = sections.get("experience", "")
    exp_score, exp_issues, bullet_rewrites = analyze_experience(exp_text)
    
    # Evaluate projects
    proj_text = sections.get("projects", "")
    proj_score, proj_issues = analyze_projects(proj_text)
    
    # Evaluate language/writing
    lang_score, lang_issues = analyze_language(text)
    
    # Evaluate timeline/date consistencies
    consistency_score, consistency_issues = analyze_consistency(text)
    
    # Evaluate ATS readability
    ats_score, ats_issues = analyze_ats_readability(text, sections_found_count)
    
    # Evaluate skill evidence
    evidence_score, evidence_issues = analyze_skill_evidence(detected_skills, sections)
    
    # 4. Consolidate issues
    all_issues = (
        structure_issues +
        contact_issues +
        summary_issues +
        exp_issues +
        proj_issues +
        lang_issues +
        consistency_issues +
        ats_issues +
        evidence_issues
    )
    
    # 5. Calculate overall diagnostic scores
    # Combine sub-scores into weighted overall score
    # Structure (15%), Role relevance/Summary (25%), Skill evidence (20%), Experience quality (20%), Project quality (10%), Writing consistency/Grammar (5%), ATS readability/Formatting (5%)
    # Let's map contact + summary into role relevance (25%)
    role_relevance_score = round(contact_score * 0.3 + summary_score * 0.7)
    
    overall_score, component_scores = calculate_quality_score(
        structure_score=structure_score,
        role_relevance_score=role_relevance_score,
        skill_evidence_score=evidence_score,
        experience_score=exp_score,
        project_score=proj_score,
        consistency_score=min(lang_score, consistency_score),
        ats_readability_score=ats_score
    )
    
    # Sort issues by severity (critical first, then important, then suggestion)
    severity_order = {"critical": 0, "important": 1, "suggestion": 2}
    all_issues.sort(key=lambda x: severity_order.get(x["severity"], 3))
    
    # Prioritize top 3 fixes
    top_fixes = []
    for issue in all_issues:
        if issue["severity"] in {"critical", "important"}:
            top_fixes.append(issue["recommendation"])
            if len(top_fixes) == 3:
                break
                
    # Fallback to secondary suggestions if less than 3 critical/important issues
    if len(top_fixes) < 3:
        for issue in all_issues:
            if issue["recommendation"] not in top_fixes:
                top_fixes.append(issue["recommendation"])
                if len(top_fixes) == 3:
                    break
                    
    # Return structured dict
    return {
        "overall_score": overall_score,
        "scores": component_scores,
        "deductions": [f"{issue['title']}: {issue['recommendation']}" for issue in all_issues],
        "issues": all_issues,
        "bullet_rewrites": bullet_rewrites,
        "top_fixes": top_fixes,
        "contact": parsed_contact,
        "sections": {sec: bool(content.strip()) for sec, content in sections.items()}
    }
