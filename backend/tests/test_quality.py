from app.services.resume_quality.analyzer import run_quality_analysis

def test_resume_quality_vague_bullets():
    text = """
    Alex Doe | alex@example.com | 123-456-7890
    SUMMARY
    Software developer building apps.
    SKILLS
    Python, FastAPI
    EXPERIENCE
    Responsible for backend development. Worked on frontend.
    """
    quality = run_quality_analysis(text)
    
    # Assert vague bullets are detected
    rewrites = quality["bullet_rewrites"]
    assert len(rewrites) > 0
    assert any("responsible for" in r["original"].lower() for r in rewrites)
    
    # Check overall score is affected by missing metrics
    assert quality["overall_score"] < 100

def test_date_timeline_contradiction():
    text = """
    Alex Doe | alex@example.com | 123-456-7890
    SUMMARY
    Software developer building apps.
    EXPERIENCE
    Software Engineer (Jan 2025 - Dec 2024)
    """
    quality = run_quality_analysis(text)
    issues = quality["issues"]
    
    # Assert date contradiction is flagged
    assert any("Date timeline contradiction" in i["title"] for i in issues)
