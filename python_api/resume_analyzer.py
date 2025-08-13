import re
from typing import List, Dict, Any

# Import from the new utils.py file
from utils import download_file, extract_text_from_pdf, TECH_SKILLS, nlp

def extract_skills(text: str) -> List[str]:
    """Extracts predefined technical skills from a given text using spaCy and a more flexible matching approach."""
    processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    
    doc = nlp(processed_text)
    found_skills = set()
    
    for token in doc:
        if token.lemma_ in TECH_SKILLS:
            found_skills.add(token.lemma_)
    
    for skill_phrase in TECH_SKILLS:
        if " " in skill_phrase:
            if re.search(r'\b' + re.escape(skill_phrase) + r'\b', processed_text):
                found_skills.add(skill_phrase)

    normalization_map = {
    # Programming Abbreviations
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "pyt": "pytorch",
    "tf": "tensorflow",
    "rb": "ruby",
    "cpp": "c++",
    "csharp": "c#",
    "golang": "go",
    "ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
    "ai": "artificial intelligence",

    # Backend Aliases
    "node": "nodejs",
    "express.js": "express",
    "nest": "nestjs",
    "springboot": "spring boot",

    # Database Aliases
    "mongo": "mongodb",
    "postgres": "postgresql",
    "maria": "mariadb",
    "dynamo": "dynamodb",

    # Cloud Aliases
    "gcp": "google cloud platform",
    "aws": "amazon web services",
    "azure": "microsoft azure",
    "ec2": "ec2",
    "s3": "s3",

    # Tools
    "ci": "ci/cd",
    "cd": "ci/cd",
    "gh": "github",
    "git hub": "github",
    "git lab": "gitlab",
    "bit bucket": "bitbucket"
}
    
    normalized_skills = {normalization_map.get(skill, skill) for skill in found_skills}

    return sorted(list(normalized_skills))

def analyze_resume_fit(resume_url: str, job_description: str) -> Dict[str, Any]:
    """
    Analyzes a resume against a job description and provides an 'explainable' match report.
    """
    try:
        resume_file = download_file(resume_url)
        resume_text = extract_text_from_pdf(resume_file)

        resume_skills = set(extract_skills(resume_text))
        job_skills = set(extract_skills(job_description.lower()))

        matching_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills.difference(resume_skills)

        total_relevant_skills = len(job_skills)
        match_score = (len(matching_skills) / total_relevant_skills) * 100 if total_relevant_skills > 0 else 0

        report = {
            "overall_match_score": round(match_score, 2),
            "matching_skills": sorted(list(matching_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "actionable_suggestions": [f"The job requires '{skill}' experience. Consider adding relevant projects to your resume." for skill in missing_skills]
        }
        
        if match_score < 70:
            report["actionable_suggestions"].append("To improve your match, quantify your achievements with numbers and metrics (e.g., 'increased sales by 15%').")

        return report

    except ValueError as e:
        # Re-raising the specific error from download/extraction
        raise
    except Exception as e:
        # Catch other unexpected errors
        raise Exception(f"An unexpected error occurred during analysis: {e}")