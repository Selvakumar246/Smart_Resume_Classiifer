from app.ml.skill_extractor import extract_skills_from_text

def test_skill_extraction_technical_boundaries():
    text = "Skills: Python, Java, React, TypeScript, C++, .NET, AWS. I like JavaScript."
    results = extract_skills_from_text(text)
    detected = {r["canonical_name"] for r in results}
    
    # Assert correct detection
    assert "Python" in detected
    assert "React" in detected
    assert "C++" in detected
    assert "AWS" in detected
    
    # Assert no false positive matching for Java inside JavaScript
    assert "Java" in detected
    assert "JavaScript" in detected

def test_dot_net_and_cpp_boundaries():
    text = "We use C++ and .NET and C# in our backend services."
    results = extract_skills_from_text(text)
    detected = {r["canonical_name"] for r in results}
    
    assert "C++" in detected
    assert "C#" in detected
