from app.services.analyzer import analyze_resume


def test_software_resume_analysis():
    text = """
    Alex Doe | alex@example.com | +1 555 222 3333
    SUMMARY
    Software engineering graduate building reliable web applications.
    SKILLS
    Python, Java, React, TypeScript, FastAPI, PostgreSQL, Git, REST API, Docker
    PROJECTS
    Developed a resume analysis API using Python and FastAPI and improved processing time by 30%.
    EDUCATION
    Bachelor of Engineering in Information Technology
    EXPERIENCE
    Software engineering intern working on backend APIs and testing.
    """
    result = analyze_resume(text, "Backend Developer", "entry", "Python FastAPI PostgreSQL Docker REST API")
    assert result["classification"]["top_categories"][0]["category"] in {"Backend Developer", "Software Engineer"}
    assert result["ats"]["overall_score"] > 50
    assert result["job_match"]["match_score"] > 0
