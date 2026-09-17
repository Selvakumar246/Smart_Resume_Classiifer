import re
from app.ml.taxonomy import ACTION_VERBS

WEAK_PHRASES = {
    "worked on": "Developed / Owned",
    "helped": "Contributed to / Led",
    "responsible for": "Engineered / Directed",
    "made": "Architected / Built",
    "did": "Executed / Maintained",
    "created": "Designed and delivered",
}

def analyze_experience(experience_text: str) -> tuple[int, list[dict], list[dict]]:
    """
    Analyzes experience bullets for strength: Action verb, Technology, Outcome/Metrics.
    Returns: (score, issues, bullet_rewrites)
    """
    issues = []
    bullet_rewrites = []
    score = 100
    
    if not experience_text.strip():
        # Handled by structure, but return 0 score here
        return 0, [], []
        
    lines = [line.strip(" •-*\t") for line in experience_text.splitlines() if line.strip()]
    
    action_verb_count = 0
    metric_count = 0
    total_bullets = 0
    
    for line in lines:
        if len(line.split()) < 4:
            continue
        total_bullets += 1
        
        words = line.lower().split()
        first_word = words[0].strip(".,;:()")
        
        starts_strong = any(first_word == verb.lower() for verb in ACTION_VERBS)
        if starts_strong:
            action_verb_count += 1
            
        has_metric = bool(re.search(r"\b\d+(?:\.\d+)?%?|\b\d+x\b", line))
        if has_metric:
            metric_count += 1
            
        # Check for weak verbs and collect suggestions
        for weak, strong in WEAK_PHRASES.items():
            if weak in line.lower():
                improved = line
                # Replace the weak phrase case-insensitively
                improved = re.sub(weak, strong, improved, count=1, flags=re.I)
                improved = improved.rstrip(".") + ", resulting in [add a measurable outcome/metric]."
                bullet_rewrites.append({
                    "original": line,
                    "improved": improved
                })
                break

    # Deduct points if action verbs are missing in many bullets
    if total_bullets > 0:
        action_ratio = action_verb_count / total_bullets
        metric_ratio = metric_count / total_bullets
        
        if action_ratio < 0.6:
            score -= 15
            issues.append({
                "category": "Experience",
                "severity": "important",
                "title": "Weak action verbs",
                "evidence": "Many bullets do not start with a strong action verb.",
                "recommendation": "Begin each bullet point with a past-tense action verb (e.g. 'Optimized', 'Architected', 'Spearheaded') to demonstrate impact."
            })
            
        if metric_ratio < 0.3:
            score -= 15
            issues.append({
                "category": "Experience",
                "severity": "suggestion",
                "title": "Measurable impact missing",
                "evidence": "Fewer than 30% of bullets contain numerical outcomes or scale metrics.",
                "recommendation": "Incorporate metrics (percentages, time saved, revenue increased, scaling size) to quantify the impact of your work where possible."
            })
    else:
        score = 80  # Default if structure has experience but no readable bullets
        
    return max(0, score), issues, bullet_rewrites[:5]
