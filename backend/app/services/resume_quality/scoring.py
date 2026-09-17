def calculate_quality_score(
    structure_score: int,
    role_relevance_score: int,
    skill_evidence_score: int,
    experience_score: int,
    project_score: int,
    consistency_score: int,
    ats_readability_score: int
) -> tuple[int, dict[str, int]]:
    """
    Calculates the Resume Quality Score out of 100 based on standard diagnostic weights.
    Weights:
      - Structure: 15%
      - Role Relevance: 25%
      - Skill Evidence: 20%
      - Experience Quality: 20%
      - Project Quality: 10%
      - Writing Consistency: 5%
      - ATS Readability: 5%
    Returns: (overall_score, sub_scores)
    """
    scores = {
        "structure": max(0, min(100, structure_score)),
        "role_relevance": max(0, min(100, role_relevance_score)),
        "skill_evidence": max(0, min(100, skill_evidence_score)),
        "experience": max(0, min(100, experience_score)),
        "projects": max(0, min(100, project_score)),
        "grammar": max(0, min(100, consistency_score)),  # UI maps 'grammar' to consistency
        "formatting": max(0, min(100, ats_readability_score)) # UI maps 'formatting' to ATS readability
    }
    
    weighted_score = (
        scores["structure"] * 0.15 +
        scores["role_relevance"] * 0.25 +
        scores["skill_evidence"] * 0.20 +
        scores["experience"] * 0.20 +
        scores["projects"] * 0.10 +
        scores["grammar"] * 0.05 +
        scores["formatting"] * 0.05
    )
    
    return round(weighted_score), scores
