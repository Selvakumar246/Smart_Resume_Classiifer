def analyze_skill_gaps(detected_skills: list[str], role_profile: dict) -> list[dict]:
    """
    Compares the detected skills against the role profile core and secondary skills.
    Returns a list of gap dictionaries for missing core skills.
    """
    core_skills = [s.lower() for s in role_profile.get("core_skills", [])]
    secondary_skills = [s.lower() for s in role_profile.get("secondary_skills", [])]
    detected_set = {s.lower() for s in detected_skills}
    
    missing_core = [s for s in role_profile.get("core_skills", []) if s.lower() not in detected_set]
    
    gaps = []
    for index, skill in enumerate(missing_core):
        # Assign priorities based on position in list
        priority = "High" if index < 3 else "Medium" if index < 6 else "Low"
        
        # Heuristics for difficulty
        skill_lower = skill.lower()
        if skill_lower in {"git", "html", "css", "excel", "jira", "linux", "sql"}:
            difficulty = "Beginner"
            hours = "8–15 hours"
        elif skill_lower in {"python", "javascript", "typescript", "react", "sql", "docker"}:
            difficulty = "Intermediate"
            hours = "20–40 hours"
        else:
            difficulty = "Advanced"
            hours = "40–80 hours"
            
        gaps.append({
            "skill": skill,
            "priority": priority,
            "difficulty": difficulty,
            "estimated_learning_time": hours,
            "roadmap": [
                f"Learn {skill} core concepts and syntax.",
                f"Build a small, standalone module or tool utilizing {skill}.",
                f"Integrate {skill} into a larger portfolio project to show end-to-end usage."
            ]
        })
        
    return gaps
