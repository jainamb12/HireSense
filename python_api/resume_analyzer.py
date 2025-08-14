# import re
# from typing import List, Dict, Any

# # Import from the new utils.py file
# from utils import download_file, extract_text_from_pdf, TECH_SKILLS, nlp

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
#     # Programming Abbreviations
#     "js": "javascript",
#     "ts": "typescript",
#     "py": "python",
#     "pyt": "pytorch",
#     "tf": "tensorflow",
#     "rb": "ruby",
#     "cpp": "c++",
#     "csharp": "c#",
#     "golang": "go",
#     "ml": "machine learning",
#     "dl": "deep learning",
#     "cv": "computer vision",
#     "ai": "artificial intelligence",

#     # Backend Aliases
#     "node": "nodejs",
#     "express.js": "express",
#     "nest": "nestjs",
#     "springboot": "spring boot",

#     # Database Aliases
#     "mongo": "mongodb",
#     "postgres": "postgresql",
#     "maria": "mariadb",
#     "dynamo": "dynamodb",

#     # Cloud Aliases
#     "gcp": "google cloud platform",
#     "aws": "amazon web services",
#     "azure": "microsoft azure",
#     "ec2": "ec2",
#     "s3": "s3",

#     # Tools
#     "ci": "ci/cd",
#     "cd": "ci/cd",
#     "gh": "github",
#     "git hub": "github",
#     "git lab": "gitlab",
#     "bit bucket": "bitbucket"
# }
    
#     normalized_skills = {normalization_map.get(skill, skill) for skill in found_skills}

#     return sorted(list(normalized_skills))

# def analyze_resume_fit(resume_url: str, job_description: str) -> Dict[str, Any]:
#     """
#     Analyzes a resume against a job description and provides an 'explainable' match report.
#     """
#     try:
#         resume_file = download_file(resume_url)
#         resume_text = extract_text_from_pdf(resume_file)

#         resume_skills = set(extract_skills(resume_text))
#         job_skills = set(extract_skills(job_description.lower()))

#         matching_skills = resume_skills.intersection(job_skills)
#         missing_skills = job_skills.difference(resume_skills)

#         total_relevant_skills = len(job_skills)
#         match_score = (len(matching_skills) / total_relevant_skills) * 100 if total_relevant_skills > 0 else 0

#         report = {
#             "overall_match_score": round(match_score, 2),
#             "matching_skills": sorted(list(matching_skills)),
#             "missing_skills": sorted(list(missing_skills)),
#             "actionable_suggestions": [f"The job requires '{skill}' experience. Consider adding relevant projects to your resume." for skill in missing_skills]
#         }
        
#         if match_score < 70:
#             report["actionable_suggestions"].append("To improve your match, quantify your achievements with numbers and metrics (e.g., 'increased sales by 15%').")

#         return report

#     except ValueError as e:
#         # Re-raising the specific error from download/extraction
#         raise
#     except Exception as e:
#         # Catch other unexpected errors
#         raise Exception(f"An unexpected error occurred during analysis: {e}")



# resume_analyzer.py

import re
from typing import List, Dict, Any, Set

# Import our new categorized skills and helper function
from utils import download_file, extract_text_from_pdf, ALL_SKILLS, SKILL_CATEGORIES, nlp
# Import the semantic similarity calculator
from semantic_matcher import calculate_semantic_similarity

# This function now uses the master list of ALL_SKILLS
# def extract_skills(text: str) -> List[str]:
#     """Extracts predefined skills from a given text using spaCy and regex."""
#     processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    
#     doc = nlp(processed_text)
#     found_skills = set()
    
#     # Check for single-word skills and multi-word skills
#     for skill in ALL_SKILLS:
#         if re.search(r'\b' + re.escape(skill) + r'\b', processed_text):
#             found_skills.add(skill)

#     # Note: Normalization logic can be added here if needed, similar to your original file
#     return sorted(list(found_skills))

def extract_skills(text: str) -> List[str]:
    """
    Extracts predefined skills from a given text using spaCy's lemmatization
    for single words and regex for multi-word phrases.
    """
    processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    
    # Run the text through the spaCy model
    doc = nlp(processed_text)
    found_skills = set()
    
    # --- The Correct Logic ---
    # 1. Use spaCy's lemmatization for efficient single-word skill matching
    for token in doc:
        # Check the base form of the word (lemma) against our skills list
        if token.lemma_ in ALL_SKILLS:
            found_skills.add(token.lemma_)

    # 2. Use regex for multi-word skills that lemmatization might miss
    for skill in ALL_SKILLS:
        if " " in skill: # Only check for phrases
            if re.search(r'\b' + re.escape(skill) + r'\b', processed_text):
                found_skills.add(skill)

    # Note: Normalization logic can be added here if needed
    return sorted(list(found_skills))

def generate_smart_advice(missing_skills: Set[str]) -> List[str]:
    """Generates contextual advice based on the category of the missing skill."""
    suggestions = []
    for skill in sorted(list(missing_skills)):
        if skill in SKILL_CATEGORIES["technical"]:
            suggestions.append(f"For the critical technical skill '{skill}', consider showcasing a project or detailing your experience with it in a past role.")
        elif skill in SKILL_CATEGORIES["soft_skills"]:
            suggestions.append(f"To demonstrate '{skill}', describe a situation where you successfully used this skill, such as in a team project or a client-facing role.")
        elif skill in SKILL_CATEGORIES["tools"]:
            suggestions.append(f"Mention how you used tools like '{skill}' to improve processes or collaborate effectively in your project descriptions.")
        else:
            suggestions.append(f"Consider gaining experience or a certification in '{skill}' to meet job requirements.")
    return suggestions

def analyze_resume_fit(resume_url: str, job_description: str, job_requirements: List[str]) -> Dict[str, Any]:
    """
    Analyzes a resume against a job description using a hybrid semantic and keyword approach.
    """
    try:
        resume_file = download_file(resume_url)
        resume_text = extract_text_from_pdf(resume_file)
        resume_skills = set(extract_skills(resume_text))
        
        # --- Step 1: Calculate the main semantic "Overall Fit" score ---
        full_job_text = job_description + " " + " ".join(job_requirements)
        overall_fit_score = calculate_semantic_similarity(resume_text, full_job_text)
        
        # --- Step 2: Perform keyword analysis to find specific missing skills ---
        must_have_skills = set(extract_skills(" ".join(job_requirements).lower()))
        missing_must_haves = must_have_skills - resume_skills

        description_skills = set(extract_skills(job_description.lower()))
        good_to_have_skills = description_skills - must_have_skills
        missing_good_to_haves = good_to_have_skills - resume_skills
        
        # --- Step 3: Generate smart, contextual advice based on must-haves ---
        suggestions = generate_smart_advice(missing_must_haves)

        # --- Step 4: Build the final, powerful report ---
        report = {
            "overall_fit_score": overall_fit_score,
            "missing_must_have_skills": sorted(list(missing_must_haves)),
            "missing_good_to_have_skills": sorted(list(missing_good_to_haves)),
            "actionable_suggestions": suggestions
        }
        
        return report

    except ValueError as e:
        raise
    except Exception as e:
        raise Exception(f"An unexpected error occurred during analysis: {e}")