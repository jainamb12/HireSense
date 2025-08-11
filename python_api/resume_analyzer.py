# # resume_analyzer.py
# import spacy
# import re
# from typing import List, Dict, Any
# from io import BytesIO

# # Make sure to import the utility functions from your main file or a shared utils file
# from main import download_file, extract_text_from_pdf, TECH_SKILLS, nlp

# def extract_skills(text: str) -> List[str]:
#     """Extracts predefined technical skills from a given text using spaCy and a more flexible matching approach."""
#     processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    
#     doc = nlp(processed_text)
#     found_skills = set()
    
#     for token in doc:
#         if token.lemma_ in TECH_SKILLS:
#             found_skills.add(token.lemma_)
    
#     for skill_phrase in TECH_SKILLS:
#         if " " in skill_phrase:
#             if re.search(r'\b' + re.escape(skill_phrase) + r'\b', processed_text):
#                 found_skills.add(skill_phrase)

#     normalization_map = {
#         "node": "nodejs",
#         "react": "react",
#         "mongo": "mongodb",
#         "postgres": "postgresql",
#         "git": "git",
#         "ci/cd": "ci/cd",
#         "express": "express",
#         "javascript": "javascript",
#         "html": "html",
#         "css": "css",
#     }
    
#     normalized_skills = set()
#     for skill in found_skills:
#         normalized_skills.add(normalization_map.get(skill, skill))

#     return sorted(list(normalized_skills))

# def analyze_resume_fit(resume_url: str, job_description: str) -> Dict[str, Any]:
#     """
#     Analyzes a resume against a job description and provides an 'explainable' match report.
#     """
#     try:
#         resume_file = download_file(resume_url)
#         resume_text = extract_text_from_pdf(resume_file)

#         resume_skills = set(extract_skills(resume_text))
        
#         job_desc_str = job_description.lower()
#         job_skills = set(extract_skills(job_desc_str))

#         matching_skills = resume_skills.intersection(job_skills)
#         missing_skills = job_skills.difference(resume_skills)

#         total_relevant_skills = len(job_skills)
#         match_score = 0
#         if total_relevant_skills > 0:
#             match_score = (len(matching_skills) / total_relevant_skills) * 100

#         report = {
#             "overall_match_score": round(match_score, 2),
#             "matching_skills": sorted(list(matching_skills)),
#             "missing_skills": sorted(list(missing_skills)),
#             "actionable_suggestions": []
#         }

#         for skill in missing_skills:
#             report["actionable_suggestions"].append(f"The job requires '{skill}' experience. Consider adding any relevant projects or work experience to your resume.")
        
#         if match_score < 70:
#             report["actionable_suggestions"].append("To improve your match, quantify your achievements with numbers and metrics (e.g., 'increased sales by 15%').")

#         return report

#     except ValueError as e:
#         raise ValueError(f"An error occurred during analysis: {e}")
#     except Exception as e:
#         raise Exception(f"An unexpected error occurred: {e}")



# resume_analyzer.py
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

    # Note: Your normalization map has some redundancy, but we'll leave it for now.
    normalization_map = {
        "node": "nodejs",
        "mongo": "mongodb",
        "postgres": "postgresql",
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