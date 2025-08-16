import re
from typing import List, Dict, Any, Set
from utils import ALL_SKILLS, SKILL_CATEGORIES, nlp
from semantic_matcher import calculate_semantic_similarity
from utils import load_resume_text
from utils import SINGLE_WORD_SKILLS, MULTI_WORD_SKILLS

def extract_skills(text: str) -> List[str]:
    processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    doc = nlp(processed_text)
    found_skills = set()
    # 1. Use spaCy's lemmatization for efficient single-word skill matching
    for token in doc:
        # Check the base form of the word (lemma) against our skills list
        if token.lemma_ in SINGLE_WORD_SKILLS:
            found_skills.add(token.lemma_)

    # 2. Use regex for multi-word skills that lemmatization might miss
    for skill in MULTI_WORD_SKILLS:
        if " " in skill: # Only check for phrases
            pattern = r'\b' + r'\s*'.join(re.escape(c) for c in skill) + r'\b'
            if re.search(pattern, processed_text, re.IGNORECASE):
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