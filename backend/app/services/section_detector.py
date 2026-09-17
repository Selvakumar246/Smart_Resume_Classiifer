import re

SECTION_HEADERS = {
    "contact": [r"^contact(info|details)?$", r"^personal(info|details)?$"],
    "summary": [r"^summary$", r"^professional\s+summary$", r"^objective$", r"^career\s+objective$", r"^profile$", r"^about\s+me$"],
    "education": [r"^education$", r"^academic\s+background$", r"^qualification(s)?$", r"^degrees$"],
    "skills": [r"^skills$", r"^technical\s+skills$", r"^core\s+competencies$", r"^expertise$", r"^technologies$", r"^skills\s+&\s+expertise$"],
    "experience": [r"^experience$", r"^work\s+experience$", r"^employment\s+history$", r"^work\s+history$", r"^professional\s+experience$", r"^internships$", r"^internship$"],
    "projects": [r"^projects$", r"^academic\s+projects$", r"^personal\s+projects$", r"^selected\s+projects$"],
    "certifications": [r"^certifications$", r"^certificates$", r"^courses$", r"^credentials$"],
    "achievements": [r"^achievements$", r"^awards$", r"^honors$"],
    "publications": [r"^publications$", r"^patents$", r"^papers$"],
    "languages": [r"^languages$", r"^linguistic\s+skills$"]
}

def detect_sections(text: str) -> dict[str, str]:
    """
    Partitions the resume text into standard sections.
    Returns a dict with section names as keys and the text content as values.
    """
    lines = text.splitlines()
    sections = {
        "contact": [],
        "summary": [],
        "education": [],
        "skills": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "achievements": [],
        "publications": [],
        "languages": []
    }
    
    current_section = "contact"  # Default to contact section for any header text
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
            
        # Check if line looks like a header (e.g. short line)
        is_header = False
        if len(cleaned_line) < 35:
            # Strip punctuation like colons, dashes, etc. for matching
            header_candidate = re.sub(r"[\-:\*•\t]", "", cleaned_line).strip().lower()
            # Remove double spaces
            header_candidate = re.sub(r"\s+", " ", header_candidate)
            
            for sec_name, patterns in SECTION_HEADERS.items():
                if any(re.match(pattern, header_candidate) for pattern in patterns):
                    current_section = sec_name
                    is_header = True
                    break
                    
        if not is_header:
            sections[current_section].append(line)
            
    # Join the lines back together
    return {sec: "\n".join(content).strip() for sec, content in sections.items()}
