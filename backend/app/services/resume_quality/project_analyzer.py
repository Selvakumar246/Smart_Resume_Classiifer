import re

def analyze_projects(projects_text: str) -> tuple[int, list[dict]]:
    """
    Analyzes project descriptions for detail level and clarity.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    
    if not projects_text.strip():
        return 0, []
        
    lines = [line.strip(" •-*\t") for line in projects_text.splitlines() if line.strip()]
    
    weak_count = 0
    for line in lines:
        if len(line.split()) < 4:
            continue
            
        # Flag overly brief or simple descriptions
        # e.g., "Resume classifier using Python and React."
        if len(line.split()) <= 10 and any(keyword in line.lower() for keyword in {"using", "built with", "developed in", "made with"}):
            weak_count += 1
            if weak_count <= 2:
                issues.append({
                    "category": "Projects",
                    "severity": "important",
                    "title": "Vague project details",
                    "evidence": line,
                    "recommendation": "Explain the specific problem solved, your contribution, and the results achieved, instead of just listing the stack."
                })
                
    if weak_count > 0:
        score -= min(20, weak_count * 10)
        
    return max(0, score), issues
