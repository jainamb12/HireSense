# # from fastapi import FastAPI, Query
# # from pydantic import BaseModel, Field
# # from typing import List, Optional
# # from resume_matcher import match_resume_to_jobs

# # app = FastAPI()


# # class Company(BaseModel):
# #     _id: str
# #     name: str


# # class Job(BaseModel):
# #     id: str = Field(..., alias="_id")
# #     title: str
# #     requirements: List[str]
# #     description: str
# #     # position: Optional[str] = None
# #     # jobType: Optional[str] = None
# #     # salary: Optional[str] = None
# #     # createdAt: Optional[str] = None
# #     company: Company


# # class MatchRequest(BaseModel):
# #     resume_url: str
# #     jobs: List[Job]


# # @app.post("/match-jobs")
# # def match_jobs(request: MatchRequest):
# #     matched = match_resume_to_jobs(request.resume_url, [job.dict() for job in request.jobs])
# #     return {"matched_jobs": matched}



# from fastapi import FastAPI, Query
# from pydantic import BaseModel, Field
# from typing import List, Optional
# from datetime import datetime # Import datetime for date parsing
# from resume_matcher import match_resume_to_jobs

# # Assuming match_resume_to_jobs is in a separate file or defined below this.
# # from resume_matcher import match_resume_to_jobs

# app = FastAPI()

# # Company schema as per your Node.js payload, assuming it's what's pulled from MongoDB
# # Make sure your Company Mongoose schema matches what you populate here.
# class Company(BaseModel):
#     # If your company is directly embedded, you might not have an _id for it in the payload.
#     # But since you are populating 'company', it will have its own _id.
#     # However, your current Node.js payload only sends 'name' and 'logo' for company.
#     # If you need the company _id in the payload, you'd have to include it in the Node.js map.
#     # For now, let's stick to what's in your current JS payload.
#     name: str
#     logo: Optional[str] = None # Assuming 'logo' is a field you might pull for company

# class Job(BaseModel):
#     # Mapped from Mongoose's _id
#     id: str = Field(..., alias="_id")

#     title: str
#     description: str
#     requirements: List[str]

#     # Changed type to float as salary is Number in Mongoose
#     salary: float

#     # Added new fields from Mongoose schema
#     experienceLevel: int # Mongoose Number maps to Python int/float
#     location: str

#     jobType: str
#     # Changed type to int as position is Number in Mongoose
#     position: int

#     # Mongoose ObjectId references are just the ID string in the payload
#     # Your Node.js code sends only company name/logo, not the ObjectId.
#     # So, keep this as a nested Pydantic model.
#     company: Company

#     # createdAt from Mongoose timestamps is a Date object, sent as ISO string.
#     # It's always present due to timestamps:true, but making it Optional[datetime]
#     # is safer if your Node.js select doesn't explicitly include it, though it should.
#     createdAt: Optional[datetime] = None

#     # Note: `created_by` and `applications` are not in your current Node.js `select`
#     # for `jobs`, so they should NOT be in your Pydantic model if you're not sending them.
#     # If you later decide to send them, add them as:
#     # created_by: Optional[str] = None # For ObjectId string
#     # applications: Optional[List[str]] = None # For array of ObjectId strings

# class MatchRequest(BaseModel):
#     resume_url: str
#     jobs: List[Job]

# @app.post("/match-jobs")
# def match_jobs(request: MatchRequest):
#     # Ensure your `match_resume_to_jobs` function is correctly imported or defined.
#     # When you pass `job.model_dump(by_alias=True)`, it converts the Pydantic Job model
#     # back into a dictionary, using '_id' for the 'id' field, which matches the expected
#     # input structure if your `match_resume_to_jobs` function relies on `_id`.
#     matched = match_resume_to_jobs(request.resume_url, [job.model_dump(by_alias=True) for job in request.jobs])
#     return {"matched_jobs": matched}

# # ... (rest of your resume_matcher.py or functions if in the same file)


# main.py
# from fastapi import FastAPI
# from pydantic import BaseModel, Field
# from typing import List, Optional
# from datetime import datetime
# import requests
# from io import BytesIO
# from pdfminer.high_level import extract_text
# import spacy
# import re
# from collections import Counter
# from resume_matcher import match_resume_to_jobs
# from resume_analyzer import analyze_resume_fit
# app = FastAPI()

# # Load the spaCy model
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("Downloading spaCy model 'en_core_web_sm'...")
#     from spacy.cli import download
#     download("en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")

# # Your existing Pydantic models
# class Company(BaseModel):
#     name: str
#     logo: Optional[str] = None

# class Job(BaseModel):
#     id: str = Field(..., alias="_id")
#     title: str
#     requirements: List[str]
#     description: str
#     salary: Optional[float] = None
#     experienceLevel: Optional[int] = None
#     location: Optional[str] = None
#     jobType: Optional[str] = None
#     position: Optional[int] = None
#     company: Company
#     createdAt: Optional[datetime] = None

# class MatchRequest(BaseModel):
#     resume_url: str
#     jobs: List[Job]

# # A new Pydantic model for the request to the new endpoint
# class ResumeAnalysisRequest(BaseModel):
#     resume_url: str
#     job_description: str

# # A simple list of common tech skills and buzzwords for demonstration
# # In a real-world scenario, this list would be much larger or dynamically generated
# # A much larger list of common skills for a more robust demo
# # A more robust list of skills, including common variations and related terms
# TECH_SKILLS = {
#     # Programming Languages
#     "python", "javascript", "typescript", "java", "c#", "c++", "ruby", "go", "swift", "php", "html", "css", "sql", "r", "rust", "kotlin", "perl", "golang",
#     "c", "matlab",

#     # Web Development Frameworks & Libraries
#     "react", "angular", "vue", "django", "flask", "express", "nodejs", "node", "next.js", "nuxt.js", "nest.js",
#     "spring", "spring boot", "ruby on rails", ".net", "asp.net", "tailwind css", "bootstrap", "jquery", "sass", "less",

#     # Cloud & DevOps
#     "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud platform", "docker", "kubernetes", "jenkins", "gitlab",
#     "terraform", "ansible", "ci/cd", "devops", "cloud computing", "lambda", "ec2", "s3", "azure devops",

#     # Databases
#     "mongodb", "mongo", "mysql", "postgresql", "postgres", "sql server", "sqlite", "oracle", "cassandra", "redis", "firebase",

#     # Data Science & Machine Learning
#     "machine learning", "ai", "artificial intelligence", "data science", "nlp", "natural language processing", "deep learning",
#     "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
#     "data visualization", "powerbi", "tableau", "spark", "hadoop",

#     # Cybersecurity
#     "cybersecurity", "network security", "firewall", "encryption",
#     "cryptography", "malware analysis", "penetration testing",
#     "incident response", "vulnerability assessment", "forensics",
#     "siem", "security information and event management",

#     # Tools & Methodologies
#     "git", "github", "gitlab", "jira", "agile", "scrum", "kanban", "restful apis", "rest", "api", "microservices", "unit testing", "tdd",
#     "documentation", "graphql", "postman", "oauth", "jira", "confluence",

#     # Soft Skills
#     "communication", "teamwork", "problem-solving", "critical thinking",
#     "adaptability", "leadership", "collaboration", "time management",
#     "project management", "attention to detail", "creative", "analytical",
# }
# def download_file(url: str) -> BytesIO:
#     """Downloads a file from a URL."""
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         return BytesIO(response.content)
#     except requests.RequestException as e:
#         raise ValueError(f"Failed to download file from {url}: {e}")

# def extract_text_from_pdf(file_obj: BytesIO) -> str:
#     """Extracts text from a PDF file object."""
#     try:
#         return extract_text(file_obj)
#     except Exception as e:
#         raise ValueError(f"Failed to extract text from PDF: {e}")

# # main.py
# # ... (rest of the code remains the same)

# def extract_skills(text: str) -> List[str]:
#     """Extracts predefined technical skills from a given text using spaCy and a more flexible matching approach."""
#     # Preprocess text to handle common variations
#     processed_text = text.lower().replace('.', ' ').replace('-', ' ')
    
#     doc = nlp(processed_text)
#     found_skills = set()
    
#     # 1. Simple keyword matching for single-word skills
#     for token in doc:
#         # Use token.lemma_ for lemmatization to handle different forms of a word (e.g., 'analyzing' -> 'analyze')
#         if token.lemma_ in TECH_SKILLS:
#             found_skills.add(token.lemma_)
    
#     # 2. Match multi-word phrases from the TECH_SKILLS list
#     # This is important for terms like "machine learning" or "restful apis"
#     for skill_phrase in TECH_SKILLS:
#         if " " in skill_phrase:
#             # Check if the multi-word phrase exists in the processed text
#             if re.search(r'\b' + re.escape(skill_phrase) + r'\b', processed_text):
#                 found_skills.add(skill_phrase)

#     # Clean up the output to be more consistent
#     # For example, map 'node' back to 'Node.js' if it was a match
#     # This is a basic form of skill normalization
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

# # ... (rest of the code remains the same)

# @app.post("/analyze-resume-fit")
# async def analyze_resume_fit(request: ResumeAnalysisRequest):
#     """
#     Analyzes a resume against a job description and provides an 'explainable' match report.
#     """
#     try:
#         # 1. Download and extract text from resume
#         resume_file = download_file(request.resume_url)
#         resume_text = extract_text_from_pdf(resume_file)

#         # 2. Extract skills from both documents
#         resume_skills = set(extract_skills(resume_text))
        
#         # Tokenize job description for cleaner comparison
#         # Cleaned up requirements list from our previous discussion
#         job_desc_str = request.job_description.lower()
#         job_skills = set(extract_skills(job_desc_str))

#         # 3. Perform comparison
#         matching_skills = resume_skills.intersection(job_skills)
#         missing_skills = job_skills.difference(resume_skills)

#         # Calculate a simple match percentage
#         total_relevant_skills = len(job_skills)
#         match_score = 0
#         if total_relevant_skills > 0:
#             match_score = (len(matching_skills) / total_relevant_skills) * 100

#         # 4. Generate the explainable report
#         report = {
#             "overall_match_score": round(match_score, 2),
#             "matching_skills": sorted(list(matching_skills)),
#             "missing_skills": sorted(list(missing_skills)),
#             "actionable_suggestions": []
#         }

#         # Add actionable suggestions for missing skills
#         for skill in missing_skills:
#             report["actionable_suggestions"].append(f"The job requires '{skill}' experience. Consider adding any relevant projects or work experience to your resume.")
        
#         # Add a generic tip
#         if match_score < 70:
#             report["actionable_suggestions"].append("To improve your match, quantify your achievements with numbers and metrics (e.g., 'increased sales by 15%').")

#         return report

#     except ValueError as e:
#         # Catch errors from download or PDF extraction
#         return {"error": str(e)}, 400
#     except Exception as e:
#         return {"error": f"An unexpected error occurred: {e}"}, 500

# # Your existing /match-jobs endpoint
# @app.post("/match-jobs")
# def match_jobs(request: MatchRequest):
# #     # Ensure your `match_resume_to_jobs` function is correctly imported or defined.
# #     # When you pass `job.model_dump(by_alias=True)`, it converts the Pydantic Job model
# #     # back into a dictionary, using '_id' for the 'id' field, which matches the expected
# #     # input structure if your `match_resume_to_jobs` function relies on `_id`.
#     matched = match_resume_to_jobs(request.resume_url, [job.model_dump(by_alias=True) for job in request.jobs])
#     return {"matched_jobs": matched}


# main.py

# from fastapi import FastAPI, Query, HTTPException
# from pydantic import BaseModel, Field
# from typing import List, Optional, Dict, Any
# from datetime import datetime
# import requests
# from io import BytesIO
# from pdfminer.high_level import extract_text
# import spacy
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from collections import Counter
# # Import the functions from your separate files
# from resume_matcher import match_resume_to_jobs
# from resume_analyzer import analyze_resume_fit as analyze_resume_fit_logic

# # --- FastAPI App ---
# app = FastAPI()

# # --- SpaCy and TECH_SKILLS ---
# try:
#     nlp = spacy.load("en_core_web_sm")
# except OSError:
#     print("Downloading spaCy model 'en_core_web_sm'...")
#     from spacy.cli import download
#     download("en_core_web_sm")
#     nlp = spacy.load("en_core_web_sm")

# TECH_SKILLS = {
#     # ... (Your comprehensive TECH_SKILLS list)
#     "python", "javascript", "typescript", "java", "c#", "c++", "ruby", "go",
#     "swift", "php", "html", "css", "sql", "r", "rust", "kotlin", "perl", "golang",
#     "c", "matlab", "react", "angular", "vue", "django", "flask", "express",
#     "nodejs", "node", "next.js", "nuxt.js", "nest.js", "spring", "spring boot",
#     "ruby on rails", ".net", "asp.net", "tailwind css", "bootstrap", "jquery",
#     "sass", "less", "aws", "amazon web services", "azure", "microsoft azure",
#     "gcp", "google cloud platform", "docker", "kubernetes", "jenkins", "gitlab",
#     "terraform", "ansible", "ci/cd", "devops", "cloud computing", "lambda", "ec2",
#     "s3", "azure devops", "mongodb", "mongo", "mysql", "postgresql", "postgres",
#     "sql server", "sqlite", "oracle", "cassandra", "redis", "firebase",
#     "machine learning", "ai", "artificial intelligence", "data science", "nlp",
#     "natural language processing", "deep learning", "pandas", "numpy", "scikit-learn",
#     "tensorflow", "pytorch", "data visualization", "powerbi", "tableau", "spark",
#     "hadoop", "cybersecurity", "network security", "firewall", "encryption",
#     "cryptography", "malware analysis", "penetration testing", "incident response",
#     "vulnerability assessment", "forensics", "siem", "security information and event management",
#     "git", "github", "gitlab", "jira", "agile", "scrum", "kanban", "restful apis",
#     "rest", "api", "microservices", "unit testing", "tdd", "documentation", "graphql",
#     "postman", "oauth", "jira", "confluence", "communication", "teamwork",
#     "problem-solving", "critical thinking", "adaptability", "leadership",
#     "collaboration", "time management", "project management", "attention to detail",
#     "creative", "analytical",
# }

# # --- Pydantic Models ---
# class Company(BaseModel):
#     name: str
#     logo: Optional[str] = None

# class Job(BaseModel):
#     id: str = Field(..., alias="_id")
#     title: str
#     requirements: List[str]
#     description: str
#     salary: Optional[float] = None
#     experienceLevel: Optional[int] = None
#     location: Optional[str] = None
#     jobType: Optional[str] = None
#     position: Optional[int] = None
#     company: Company
#     createdAt: Optional[datetime] = None

# class MatchRequest(BaseModel):
#     resume_url: str
#     jobs: List[Job]

# class ResumeAnalysisRequest(BaseModel):
#     resume_url: str
#     job_description: str

# # --- Shared Utility Functions (Keep these in main.py as they are used by both features) ---
# def download_file(url: str) -> BytesIO:
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
#         return BytesIO(response.content)
#     except requests.RequestException as e:
#         raise ValueError(f"Failed to download file from {url}: {e}")

# def extract_text_from_pdf(file_obj: BytesIO) -> str:
#     try:
#         return extract_text(file_obj)
#     except Exception as e:
#         raise ValueError(f"Failed to extract text from PDF: {e}")

# # --- API Endpoints ---
# @app.post("/match-jobs")
# def match_jobs(request: MatchRequest):
#     matched = match_resume_to_jobs(request.resume_url, [job.model_dump(by_alias=True) for job in request.jobs])
#     return {"matched_jobs": matched}

# @app.post("/analyze-resume-fit")
# async def analyze_resume_fit_endpoint(request: ResumeAnalysisRequest):
#     try:
#         # Call the function from the separate file, using an alias to avoid name conflict
#         report = analyze_resume_fit_logic(request.resume_url, request.job_description)
#         return report
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# main.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Import logic from your other modules
from resume_matcher import match_resume_to_jobs
from resume_analyzer import analyze_resume_fit as analyze_resume_fit_logic
from job_analytics import get_job_analytics_data
# --- FastAPI App ---
app = FastAPI()

# --- Pydantic Models (These are specific to the API, so they stay here) ---
class Company(BaseModel):
    name: str
    logo: Optional[str] = None

class Job(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    requirements: List[str]
    description: str
    salary: Optional[float] = None
    experienceLevel: Optional[int] = None
    location: Optional[str] = None
    jobType: Optional[str] = None
    position: Optional[int] = None
    company: Company
    createdAt: Optional[datetime] = None

class MatchRequest(BaseModel):
    resume_url: str
    jobs: List[Job]

class ResumeAnalysisRequest(BaseModel):
    resume_url: str
    job_description: str

# --- API Endpoints ---
@app.post("/match-jobs")
def match_jobs(request: MatchRequest):
    try:
        # Pass the jobs list after converting Pydantic models to dictionaries
        matched = match_resume_to_jobs(request.resume_url, [job.model_dump(by_alias=True) for job in request.jobs])
        return {"matched_jobs": matched}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/analyze-resume-fit")
async def analyze_resume_fit_endpoint(request: ResumeAnalysisRequest):
    try:
        report = analyze_resume_fit_logic(request.resume_url, request.job_description)
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    
@app.get("/job-analytics")
def job_analytics_endpoint(
    location: Optional[str] = Query('all'),
    job_type: Optional[str] = Query('all')
):
    try:
        analytics_data = get_job_analytics_data(location=location, job_type=job_type)
        return analytics_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))