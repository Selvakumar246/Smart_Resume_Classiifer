import re

BOILERPLATE_PHRASES = [
    r"hardworking\s+individual",
    r"seeking\s+a\s+challenging\s+opportunity",
    r"highly\s+motivated\s+individual",
    r"results-oriented\s+professional",
    r"proven\s+track\s+record",
    r"dynamic\s+team\s+player"
]

def analyze_summary(summary_text: str, role_title: str) -> tuple[int, list[dict]]:
    """
    Evaluates summary clarity, length, and presence of generic phrases.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    
    if not summary_text.strip():
        # Handled by structure, but return 0 score here
        return 0, []
        
    words_count = len(summary_text.split())
    
    # 1. Check length
    if words_count < 15:
        score -= 10
        issues.append({
            "category": "Summary Quality",
            "severity": "important",
            "title": "Summary is too short",
            "evidence": f"Word count: {words_count}.",
            "recommendation": "Expand your summary to 2-3 sentences. Summarize your core technical background, top accomplishments, and target specialization."
        })
    elif words_count > 80:
        score -= 8
        issues.append({
            "category": "Summary Quality",
            "severity": "suggestion",
            "title": "Summary is too wordy",
            "evidence": f"Word count: {words_count}.",
            "recommendation": "Condense your summary to 3-4 lines max. Keep it focused and avoid general biographical details."
        })
        
    # 2. Check for generic boilerplate
    found_boilerplate = []
    for pattern in BOILERPLATE_PHRASES:
        if re.search(pattern, summary_text, re.I):
            found_boilerplate.append(pattern.replace(r"\s+", " "))
            
    if found_boilerplate:
        score -= 10
        issues.append({
            "category": "Summary Quality",
            "severity": "important",
            "title": "Generic boilerplate objectives detected",
            "evidence": f"Detected phrases: {', '.join(found_boilerplate[:2])}.",
            "recommendation": "Remove generic adjectives and cliches like 'hardworking individual'. Instead, open with your professional title (e.g. 'Backend Engineer with 2+ years of experience specializing in FastAPI...')."
        })
        
    # 3. Check for role alignment (if role_title is supplied)
    if role_title and role_title.lower() not in summary_text.lower():
        # We don't deduct points but we give a suggestion
        issues.append({
            "category": "Summary Quality",
            "severity": "suggestion",
            "title": "Summary lacks target role alignment",
            "evidence": f"Target role '{role_title}' was not found in the summary.",
            "recommendation": f"Customize your summary header to explicitly mention '{role_title}' or related terminology to capture immediate interest."
        })
        
    return max(0, score), issues
