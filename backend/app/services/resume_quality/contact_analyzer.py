import re

def analyze_contact_info(text: str) -> tuple[int, list[dict], dict]:
    """
    Checks for the presence of email, phone, github, and linkedin in the resume.
    Returns: (score, issues, parsed_contact)
    """
    issues = []
    score = 100
    
    # 1. Parse contact details (without logging or exposing PII)
    emails = sorted(list(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))))
    # Clean phone numbers (match typical patterns)
    phones = sorted(list(set(re.findall(r"(?:\+?\d[\d\s()-]{8,}\d)", text))))[:2]
    
    urls = re.findall(r"https?://[^\s)>,]+|(?:github\.com|linkedin\.com)/[^\s)>,]+", text, re.I)
    github = sorted(list(set([url for url in urls if "github" in url.lower()])))
    linkedin = sorted(list(set([url for url in urls if "linkedin" in url.lower()])))
    
    parsed_contact = {
        "emails": emails,
        "phones": phones,
        "github": github,
        "linkedin": linkedin,
        "urls": urls[:5]
    }
    
    # 2. Heuristic scoring
    if not emails:
        score -= 15
        issues.append({
            "category": "Contact Details",
            "severity": "critical",
            "title": "Missing email address",
            "evidence": "",
            "recommendation": "No valid email address was detected. Add a clear, professional email to your contact section."
        })
        
    if not phones:
        score -= 10
        issues.append({
            "category": "Contact Details",
            "severity": "important",
            "title": "Missing phone number",
            "evidence": "",
            "recommendation": "No contact phone number was found. Add a valid telephone number so recruiters can reach you."
        })
        
    if not linkedin:
        score -= 5
        issues.append({
            "category": "Contact Details",
            "severity": "suggestion",
            "title": "LinkedIn profile missing",
            "evidence": "",
            "recommendation": "Consider adding a link to your LinkedIn profile to showcase recommendations and professional network."
        })
        
    # We do NOT penalize missing GitHub since it is role-specific (e.g. non-programmers don't need GitHub).
    
    return max(0, score), issues, parsed_contact
