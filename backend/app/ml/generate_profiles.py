import os
import json
from pathlib import Path

ROLES = {
    "software_engineer": {
        "name": "Software Engineer",
        "category": "Software Development",
        "description": "General software engineering, object-oriented programming, testing, system design and product development.",
        "core_skills": ["Python", "Java", "C++", "C#", "Git", "REST API", "SQL"],
        "secondary_skills": ["Docker", "Go", "TypeScript", "Testing", "Algorithms", "Data Structures"],
        "concepts": ["OOP", "Design Patterns", "CI/CD", "System Design"],
        "experience_keywords": ["develop", "engineer", "software", "architecture", "codebase"]
    },
    "frontend_developer": {
        "name": "Frontend Developer",
        "category": "Software Development",
        "description": "Responsive interfaces, design systems, accessibility, web performance and browser applications.",
        "core_skills": ["HTML", "CSS", "JavaScript", "TypeScript", "React"],
        "secondary_skills": ["Next.js", "Tailwind CSS", "Redux", "Svelte", "Figma"],
        "concepts": ["Responsive Design", "Accessibility", "Web Performance", "DOM Manipulation"],
        "experience_keywords": ["frontend", "ui", "ux", "interface", "component", "styling"]
    },
    "backend_developer": {
        "name": "Backend Developer",
        "category": "Software Development",
        "description": "Server-side applications, APIs, databases, authentication, performance and distributed systems.",
        "core_skills": ["Python", "Java", "Node.js", "FastAPI", "Django", "SQL", "PostgreSQL"],
        "secondary_skills": ["Redis", "Docker", "MongoDB", "GraphQL", "Spring Boot"],
        "concepts": ["Microservices", "REST API", "Authentication", "Database Normalization", "Caching"],
        "experience_keywords": ["backend", "api", "database", "server", "endpoints", "server-side"]
    },
    "full_stack_developer": {
        "name": "Full Stack Developer",
        "category": "Software Development",
        "description": "End-to-end development of web applications, covering both frontend user interfaces and backend server/database systems.",
        "core_skills": ["JavaScript", "TypeScript", "React", "Node.js", "Express.js", "SQL", "PostgreSQL"],
        "secondary_skills": ["Next.js", "FastAPI", "MongoDB", "Docker", "REST API", "Tailwind CSS"],
        "concepts": ["Full Stack", "Client-Server", "API Integration", "State Management"],
        "experience_keywords": ["full stack", "end-to-end", "frontend", "backend", "fullstack"]
    },
    "mobile_developer": {
        "name": "Mobile Developer",
        "category": "Software Development",
        "description": "Native and cross-platform mobile application development for iOS and Android devices.",
        "core_skills": ["Kotlin", "Swift", "React Native", "Flutter", "JavaScript"],
        "secondary_skills": ["Java", "TypeScript", "REST API", "Xcode", "Android Studio"],
        "concepts": ["Mobile UI", "App Store Guidelines", "State Management", "Offline Storage"],
        "experience_keywords": ["mobile", "ios", "android", "app", "apps", "react native", "flutter"]
    },
    "data_analyst": {
        "name": "Data Analyst",
        "category": "Data & AI",
        "description": "Data collection, cleaning, processing, statistical analysis and generating business insights via reports and dashboards.",
        "core_skills": ["SQL", "Excel", "Python", "Tableau", "Power BI"],
        "secondary_skills": ["Pandas", "NumPy", "Statistics", "Data Analysis", "Matplotlib"],
        "concepts": ["Data Visualization", "Reporting", "Metrics", "Dashboards", "ETL"],
        "experience_keywords": ["analytics", "analyst", "insights", "data", "reporting", "dashboard"]
    },
    "data_scientist": {
        "name": "Data Scientist",
        "category": "Data & AI",
        "description": "Statistical analysis, experimentation, predictive modeling, data visualization and business insights.",
        "core_skills": ["Python", "Pandas", "NumPy", "Statistics", "Machine Learning", "SQL"],
        "secondary_skills": ["Scikit-learn", "Matplotlib", "Seaborn", "Tableau", "R"],
        "concepts": ["Predictive Modeling", "Hypothesis Testing", "Regression", "Classification"],
        "experience_keywords": ["data science", "scientist", "statistical", "experiments", "predictive"]
    },
    "machine_learning_engineer": {
        "name": "Machine Learning Engineer",
        "category": "Data & AI",
        "description": "Production machine learning, feature engineering, model training, evaluation, deployment and MLOps.",
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Scikit-learn"],
        "secondary_skills": ["MLOps", "Docker", "Kubernetes", "Linux", "SQL", "Pandas"],
        "concepts": ["Model Serving", "Feature Engineering", "Neural Networks", "Hyperparameter Tuning"],
        "experience_keywords": ["ml", "machine learning", "model deployment", "training", "pipeline", "mlops"]
    },
    "data_engineer": {
        "name": "Data Engineer",
        "category": "Data & AI",
        "description": "Designing and building pipelines for data ingestion, processing, warehousing, and analytics infrastructure.",
        "core_skills": ["Python", "SQL", "PostgreSQL", "AWS", "Spark"],
        "secondary_skills": ["Docker", "Kubernetes", "Linux", "Airflow", "Kafka"],
        "concepts": ["ETL", "Data Pipelines", "Data Warehousing", "Data Lake", "Big Data"],
        "experience_keywords": ["data pipeline", "pipelines", "etl", "warehouse", "ingestion"]
    },
    "devops_engineer": {
        "name": "DevOps Engineer",
        "category": "Infrastructure",
        "description": "CI/CD, infrastructure automation, containers, observability, release engineering and reliability.",
        "core_skills": ["Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions", "Linux"],
        "secondary_skills": ["AWS", "CI/CD", "Ansible", "Prometheus", "Grafana"],
        "concepts": ["Infrastructure as Code", "Continuous Integration", "Monitoring", "Automation"],
        "experience_keywords": ["devops", "pipeline", "ci/cd", "automation", "kubernetes", "infrastructure"]
    },
    "cloud_engineer": {
        "name": "Cloud Engineer",
        "category": "Infrastructure",
        "description": "Cloud infrastructure, scalable services, networking, automation, reliability and cost optimization.",
        "core_skills": ["AWS", "Azure", "GCP", "Linux", "Terraform"],
        "secondary_skills": ["Docker", "Kubernetes", "CloudFormation", "IAM", "Networking"],
        "concepts": ["Cloud Architecture", "Serverless", "Security Groups", "Virtual Private Cloud"],
        "experience_keywords": ["cloud", "aws", "azure", "gcp", "hosting", "migration"]
    },
    "cybersecurity_analyst": {
        "name": "Cybersecurity Analyst",
        "category": "Security & Networking",
        "description": "Security operations, vulnerability assessment, secure systems, incident response and risk management.",
        "core_skills": ["Network Security", "SIEM", "Penetration Testing", "OWASP", "Linux"],
        "secondary_skills": ["Wireshark", "Burp Suite", "Cryptography", "IAM", "Networking"],
        "concepts": ["Threat Analysis", "Incident Response", "Vulnerability Management", "Access Control"],
        "experience_keywords": ["security", "cybersecurity", "vulnerability", "threat", "penetration", "incident"]
    },
    "network_engineer": {
        "name": "Network Engineer",
        "category": "Security & Networking",
        "description": "Designing, implementing, and managing computer networks, routing, switching, and firewall security.",
        "core_skills": ["Networking", "TCP/IP", "DNS", "VPN", "Linux"],
        "secondary_skills": ["Cisco", "Firewalls", "Wireshark", "AWS", "Network Security"],
        "concepts": ["Routing Protocols", "Subnetting", "Network Topology", "Load Balancing"],
        "experience_keywords": ["network", "networks", "routing", "switching", "firewall", "cisco"]
    },
    "database_administrator": {
        "name": "Database Administrator",
        "category": "Databases",
        "description": "Managing, securing, optimizing, backing up, and troubleshooting relational and non-relational database systems.",
        "core_skills": ["SQL", "PostgreSQL", "MySQL", "Oracle", "Linux"],
        "secondary_skills": ["Redis", "MongoDB", "Cassandra", "AWS", "Scripting"],
        "concepts": ["Database Administration", "Backup & Recovery", "Query Optimization", "High Availability"],
        "experience_keywords": ["dba", "database administrator", "database", "tuning", "optimization", "backup"]
    },
    "qa_engineer": {
        "name": "QA Engineer",
        "category": "Software Development",
        "description": "Quality assurance, manual and automated testing, bug tracking, and release quality verification.",
        "core_skills": ["Testing", "Unit Testing", "Integration Testing", "Selenium", "Cypress", "Git"],
        "secondary_skills": ["Jest", "JavaScript", "Python", "Jira", "API Testing"],
        "concepts": ["Test Automation", "Regression Testing", "SDLC", "Bug Tracking"],
        "experience_keywords": ["testing", "qa", "test", "bugs", "quality", "selenium", "cypress"]
    },
    "ui_ux_designer": {
        "name": "UI/UX Designer",
        "category": "Design",
        "description": "Creating user-centric product designs, wireframes, prototypes, user research and visual assets.",
        "core_skills": ["UI/UX Design", "Figma", "Adobe XD", "Sketch", "Wireframing"],
        "secondary_skills": ["HTML", "CSS", "User Research", "Prototyping", "Design Systems"],
        "concepts": ["User-Centered Design", "Interaction Design", "Visual Hierarchy", "Typography"],
        "experience_keywords": ["ui/ux", "designer", "figma", "wireframes", "prototype", "design", "user interface"]
    },
    "business_analyst": {
        "name": "Business Analyst",
        "category": "Business & Management",
        "description": "Requirements analysis, process improvement, stakeholder communication, reporting and business intelligence.",
        "core_skills": ["Business Analysis", "Requirements Gathering", "SQL", "Excel", "Jira"],
        "secondary_skills": ["Power BI", "Tableau", "Documentation", "Stakeholder Management", "Process Mapping"],
        "concepts": ["Agile Methodology", "Requirements Specification", "Gap Analysis", "UML Diagrams"],
        "experience_keywords": ["analyst", "business analyst", "requirements", "stakeholders", "process"]
    },
    "project_manager": {
        "name": "Project Manager",
        "category": "Business & Management",
        "description": "Orchestrating software projects, agile ceremonies, resource planning, sprint planning, and product delivery.",
        "core_skills": ["Project Management", "Agile", "Scrum", "Jira", "Stakeholder Management"],
        "secondary_skills": ["Product Management", "Documentation", "Excel", "Communication", "Budgets"],
        "concepts": ["Sprint Planning", "Roadmaps", "Risk Mitigation", "Agile Methodologies"],
        "experience_keywords": ["project manager", "scrum master", "agile", "delivery", "roadmap", "sprint"]
    }
}

def generate():
    target_dir = Path(__file__).parent / "role_profiles"
    target_dir.mkdir(parents=True, exist_ok=True)
    for key, val in ROLES.items():
        with open(target_dir / f"{key}.json", "w", encoding="utf-8") as f:
            json.dump(val, f, indent=2)
    print(f"Generated {len(ROLES)} role profiles in {target_dir}")

if __name__ == "__main__":
    generate()
