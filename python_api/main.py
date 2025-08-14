from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from resume_matcher import match_resume_to_jobs
from resume_analyzer import analyze_resume_fit as analyze_resume_fit_logic
from job_analytics import get_job_analytics_data

# --- FastAPI App ---
app = FastAPI()

# --- Pydantic Models ---
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
    job_requirements: List[str]

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
        report = analyze_resume_fit_logic(
            request.resume_url, 
            request.job_description,
            request.job_requirements
        )
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