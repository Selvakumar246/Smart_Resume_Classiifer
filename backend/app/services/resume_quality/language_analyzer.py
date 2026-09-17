import re

# Technical dictionary of terms that should NEVER be flagged as spelling errors (used in general filtering)
TECHNICAL_WORDS = {
    "fastapi", "pytorch", "tensorflow", "postgresql", "mongodb", "kubernetes", 
    "numpy", "javascript", "typescript", "nodejs", "nextjs", "aws", "gcp", 
    "azure", "docker", "mlops", "scikit", "pandas", "spacy", "react", "redux",
    "flask", "django", "github", "gitlab", "devops", "redis", "alembic", "uvicorn"
}

def analyze_language(text: str) -> tuple[int, list[dict]]:
    """
    Checks writing quality, repeated words, excessive first-person pronouns, and sentence length.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    lowered = text.lower()
    
    # 1. Repeated words
    repeated = re.findall(r"\b(\w+)\s+\1\b", lowered)
    # Filter out common false positives if any, e.g., "had had" can be grammatically correct, but others are typos
    repeated_typos = [word for word in repeated if word not in {"had", "that"}]
    if repeated_typos:
        score -= min(15, len(repeated_typos) * 5)
        issues.append({
            "category": "Writing Consistency",
            "severity": "critical",
            "title": "Duplicate consecutive words",
            "evidence": f"Repeated words detected: {', '.join(repeated_typos)}.",
            "recommendation": "Proofread your resume to remove accidental duplicate consecutive words."
        })
        
    # 2. First-person pronouns
    first_person = re.findall(r"\b(i|me|my|we|our|us)\b", lowered)
    if len(first_person) > 3:
        score -= 10
        issues.append({
            "category": "Writing Consistency",
            "severity": "important",
            "title": "Excessive first-person pronouns",
            "evidence": f"Detected first-person pronouns {len(first_person)} times.",
            "recommendation": "Resumes should be written in an impersonal, bulleted style (e.g. 'Implemented...' instead of 'I implemented...')."
        })
        
    # 3. Very long lines/bullets
    long_lines = [line.strip() for line in text.splitlines() if len(line.split()) > 35]
    if long_lines:
        score -= min(10, len(long_lines) * 2)
        issues.append({
            "category": "Writing Consistency",
            "severity": "suggestion",
            "title": "Extremely long sentences or bullets",
            "evidence": f"Found {len(long_lines)} lines with more than 35 words.",
            "recommendation": "Keep sentences and bullets concise (between 10 to 30 words) to ensure high readability for hiring managers."
        })
        
    return max(0, score), issues
