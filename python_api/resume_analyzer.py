import re
from typing import List, Dict, Any, Set
from utils import ALL_SKILLS, SKILL_CATEGORIES, nlp
from semantic_matcher import calculate_semantic_similarity
from utils import load_resume_text
from utils import SINGLE_WORD_SKILLS, MULTI_WORD_SKILLS, SKILL_NORMALIZATION_MAP

def extract_skills(text: str) -> List[str]:
    """
    Extracts and normalizes skills from text to handle variations.
    """
    processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    found_skills = set()

    # Search for all possible skills from our master list
    for skill in ALL_SKILLS:
        pattern = r'\b' + re.escape(skill).replace(r'\ ', r'\s*') + r'\b'
        if re.search(pattern, processed_text):
            found_skills.add(skill)
            
    # Also search for aliases from our normalization map
    for alias, standard_form in SKILL_NORMALIZATION_MAP.items():
        pattern = r'\b' + re.escape(alias).replace(r'\ ', r'\s*') + r'\b'
        if re.search(pattern, processed_text):
            found_skills.add(standard_form) # Add the standard form!

    # Final pass to normalize everything found
    normalized_found_skills = {
        SKILL_NORMALIZATION_MAP.get(skill, skill) for skill in found_skills
    }

    # Only return skills that are in our master list
    final_skills = normalized_found_skills.intersection(ALL_SKILLS)
    
    return sorted(list(final_skills))

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
        resume_text = load_resume_text(resume_url)
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