def analyze_sections(sections: dict[str, str]) -> tuple[int, list[dict]]:
    """
    Evaluates section completeness.
    Returns: (score, list of issue dicts)
    """
    issues = []
    score = 100
    
    # Vital sections list
    vital = {
        "summary": {"weight": 15, "name": "Summary / Professional Profile"},
        "skills": {"weight": 20, "name": "Skills"},
        "experience": {"weight": 25, "name": "Experience / Work History"},
        "education": {"weight": 20, "name": "Education"},
        "projects": {"weight": 20, "name": "Projects"}
    }
    
    for key, info in vital.items():
        content = sections.get(key, "").strip()
        if not content:
            score -= info["weight"]
            severity = "critical" if key in {"skills", "experience"} else "important"
            issues.append({
                "category": "Structure",
                "severity": severity,
                "title": f"Missing {info['name']} section",
                "evidence": "",
                "recommendation": f"A clear, dedicated {info['name']} section was not detected. Consider adding it to guide parser scanning."
            })
            
    return max(0, score), issues
