import re

def analyze_ats_readability(text: str, sections_found_count: int) -> tuple[int, list[dict]]:
    """
    Evaluates factors affecting parsing.
    Returns: (score, issues)
    """
    issues = []
    score = 100
    
    # 1. Unusual character corruption or encoding issues
    # e.g., unicode replacement character \ufffd or excessive symbols
    corrupt_chars = len(re.findall(r"[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    if corrupt_chars > 0:
        score -= min(20, corrupt_chars * 5)
        issues.append({
            "category": "ATS Readability",
            "severity": "critical",
            "title": "Character encoding corruption",
            "evidence": f"Detected {corrupt_chars} corrupted or unreadable characters.",
            "recommendation": "The PDF/Docx parser encountered unreadable symbols. Re-export your resume from Word or Google Docs using a standard font."
        })
        
    # 2. Too many decorative characters or lines (e.g., heavy tables, pipe symbols, boxes)
    pipe_count = text.count("|")
    if pipe_count > 25:
        score -= 10
        issues.append({
            "category": "ATS Readability",
            "severity": "important",
            "title": "Complex layout or heavy table usage",
            "evidence": f"Found {pipe_count} layout separator symbols (|).",
            "recommendation": "Many older ATS parsers struggle with multi-column tables or complex grids. Prefer a clean, single-column design."
        })
        
    # 3. Non-standard symbols or special characters
    special_chars = len(re.findall(r"[^\w\s.,:;()/%+\-#@'’\"“”]", text))
    if special_chars > 60:
        score -= 8
        issues.append({
            "category": "ATS Readability",
            "severity": "suggestion",
            "title": "Excessive visual decorative elements",
            "evidence": f"Detected {special_chars} non-standard decorative characters or icons.",
            "recommendation": "Remove graphical icons, star ratings for skills, or visual progress bars, as ATS systems cannot parse them and they may corrupt surrounding text."
        })
        
    # 4. Poor section completeness
    if sections_found_count < 3:
        score -= 15
        issues.append({
            "category": "ATS Readability",
            "severity": "important",
            "title": "Low section density",
            "evidence": f"Only detected {sections_found_count} clear headings.",
            "recommendation": "Ensure headings use standard text and are clearly separated on their own lines (e.g. 'EDUCATION', 'EXPERIENCE') so parser can index them."
        })
        
    return max(0, score), issues
