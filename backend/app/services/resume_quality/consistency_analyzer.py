import re

def analyze_consistency(text: str) -> tuple[int, list[dict]]:
    """
    Checks for date inconsistencies, duplicated lines/bullets, and keyword stuffing.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    lowered = text.lower()
    
    # 1. Date contradictions (e.g., "2025 - 2024" or "Jan 2025 - Dec 2024")
    # Let's search for patterns: Month Year - Month Year or Year - Year
    # Example: 2024 - 2023 or 2025-2024
    year_ranges = re.findall(r"\b(20\d{2})\s*[\-–—]\s*(20\d{2})\b", text)
    for start_yr, end_yr in year_ranges:
        if int(start_yr) > int(end_yr):
            score -= 15
            issues.append({
                "category": "Writing Consistency",
                "severity": "critical",
                "title": "Date timeline contradiction",
                "evidence": f"Detected range: {start_yr} - {end_yr}.",
                "recommendation": "A start date cannot be later than an end date. Review your employment dates for timeline accuracy."
            })
            break # Flag once
            
    # Check for timeline gaps in neutral wording (optional/informative)
    # We won't penalize score but we can suggest looking over dates if a range is found
    # (The prompt says: "Timeline gaps must NOT be called mistakes. Use neutral language: A timeline gap may be present. Review the dates for accuracy.")
    
    # 2. Duplicate bullets or lines
    lines = [l.strip().lower() for l in text.splitlines() if len(l.strip()) > 15]
    seen = set()
    duplicates = []
    for l in lines:
        if l in seen:
            duplicates.append(l)
        else:
            seen.add(l)
            
    if duplicates:
        score -= min(15, len(duplicates) * 5)
        issues.append({
            "category": "Writing Consistency",
            "severity": "important",
            "title": "Duplicated sentences or bullets",
            "evidence": f"Found {len(duplicates)} duplicated lines in the text.",
            "recommendation": "Remove repetitive bullets or projects that appear identical to save resume space and keep it engaging."
        })
        
    # 3. Keyword stuffing (very high count of single words, except stop words)
    words = re.findall(r"\b([a-zA-Z]{3,})\b", lowered)
    word_counts = {}
    for w in words:
        if w not in {"the", "and", "for", "with", "that", "this", "from", "your", "development", "project", "system", "using"}:
            word_counts[w] = word_counts.get(w, 0) + 1
            
    stuffed = [w for w, count in word_counts.items() if count > 12]
    if stuffed:
        score -= min(10, len(stuffed) * 2)
        issues.append({
            "category": "Writing Consistency",
            "severity": "suggestion",
            "title": "Possible keyword stuffing",
            "evidence": f"High repetition of terms like: {', '.join(stuffed[:3])}.",
            "recommendation": "Ensure technical keywords are naturally integrated into project and work descriptions rather than repeated excessively."
        })
        
    return max(0, score), issues
