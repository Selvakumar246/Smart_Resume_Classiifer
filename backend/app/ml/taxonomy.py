CATEGORY_PROFILES: dict[str, dict] = {
    "Software Engineer": {
        "description": "General software engineering, object-oriented programming, testing, system design and product development.",
        "skills": ["python", "java", "c++", "javascript", "data structures", "algorithms", "oop", "git", "testing", "system design", "rest api", "sql"],
    },
    "Data Scientist": {
        "description": "Statistical analysis, experimentation, predictive modeling, data visualization and business insights.",
        "skills": ["python", "pandas", "numpy", "statistics", "machine learning", "sql", "tableau", "power bi", "matplotlib", "scikit-learn", "experimentation"],
    },
    "AI Engineer": {
        "description": "Applied artificial intelligence, generative AI, NLP, computer vision, model serving and AI applications.",
        "skills": ["python", "deep learning", "pytorch", "tensorflow", "nlp", "computer vision", "transformers", "llm", "rag", "vector database", "fastapi"],
    },
    "Machine Learning Engineer": {
        "description": "Production machine learning, feature engineering, model training, evaluation, deployment and MLOps.",
        "skills": ["python", "scikit-learn", "pytorch", "tensorflow", "feature engineering", "mlops", "docker", "kubernetes", "airflow", "model deployment", "statistics"],
    },
    "Cloud Engineer": {
        "description": "Cloud infrastructure, scalable services, networking, automation, reliability and cost optimization.",
        "skills": ["aws", "azure", "gcp", "terraform", "docker", "kubernetes", "linux", "networking", "cloudformation", "iam", "monitoring", "serverless"],
    },
    "Backend Developer": {
        "description": "Server-side applications, APIs, databases, authentication, performance and distributed systems.",
        "skills": ["python", "java", "node.js", "fastapi", "django", "spring boot", "rest api", "graphql", "postgresql", "redis", "microservices", "authentication"],
    },
    "Frontend Developer": {
        "description": "Responsive interfaces, design systems, accessibility, web performance and browser applications.",
        "skills": ["html", "css", "javascript", "typescript", "react", "next.js", "tailwind", "redux", "accessibility", "responsive design", "figma", "web performance"],
    },
    "Cyber Security": {
        "description": "Security operations, vulnerability assessment, secure systems, incident response and risk management.",
        "skills": ["network security", "siem", "penetration testing", "owasp", "linux", "wireshark", "burp suite", "incident response", "vulnerability assessment", "cryptography", "iam"],
    },
    "DevOps Engineer": {
        "description": "CI/CD, infrastructure automation, containers, observability, release engineering and reliability.",
        "skills": ["docker", "kubernetes", "jenkins", "github actions", "terraform", "ansible", "linux", "prometheus", "grafana", "ci/cd", "aws", "scripting"],
    },
    "Business Analyst": {
        "description": "Requirements analysis, process improvement, stakeholder communication, reporting and business intelligence.",
        "skills": ["requirements gathering", "business analysis", "sql", "excel", "power bi", "tableau", "stakeholder management", "process mapping", "jira", "documentation", "data analysis"],
    },
    "Digital Marketing": {
        "description": "Performance marketing, content strategy, SEO, social media, analytics and campaign optimization.",
        "skills": ["seo", "sem", "google analytics", "content marketing", "social media", "campaign management", "copywriting", "email marketing", "conversion optimization", "meta ads"],
    },
    "Finance": {
        "description": "Financial analysis, accounting, valuation, forecasting, reporting and risk assessment.",
        "skills": ["financial analysis", "accounting", "excel", "financial modeling", "valuation", "forecasting", "budgeting", "risk management", "tally", "sap", "power bi"],
    },
    "Human Resources": {
        "description": "Talent acquisition, employee relations, performance management, HR operations and learning.",
        "skills": ["recruitment", "talent acquisition", "onboarding", "employee engagement", "performance management", "hr analytics", "payroll", "labor law", "training", "communication"],
    },
    "Mechanical Engineer": {
        "description": "Mechanical design, manufacturing, CAD, thermal systems, quality and industrial engineering.",
        "skills": ["autocad", "solidworks", "catia", "ansys", "manufacturing", "thermodynamics", "mechanical design", "quality control", "cnc", "gd&t", "matlab"],
    },
    "Civil Engineer": {
        "description": "Structural design, construction planning, surveying, estimation and infrastructure projects.",
        "skills": ["autocad", "staad pro", "revit", "structural analysis", "surveying", "construction management", "estimation", "quantity surveying", "primavera", "concrete technology"],
    },
    "Electrical Engineer": {
        "description": "Electrical systems, power electronics, control systems, embedded systems and industrial automation.",
        "skills": ["matlab", "simulink", "power systems", "control systems", "plc", "scada", "embedded systems", "circuit design", "power electronics", "iot", "microcontrollers"],
    },
}

ALL_SKILLS = sorted({skill for profile in CATEGORY_PROFILES.values() for skill in profile["skills"]}, key=len, reverse=True)

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving", "critical thinking",
    "time management", "adaptability", "collaboration", "presentation", "stakeholder management"
]

ACTION_VERBS = [
    "achieved", "automated", "built", "created", "delivered", "designed", "developed", "drove",
    "implemented", "improved", "increased", "launched", "led", "optimized", "reduced", "resolved",
    "scaled", "streamlined", "tested"
]
