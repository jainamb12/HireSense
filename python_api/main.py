# from fastapi import FastAPI, Query
# from pydantic import BaseModel, Field
# from typing import List, Optional
# from resume_matcher import match_resume_to_jobs

# app = FastAPI()


# class Company(BaseModel):
#     _id: str
#     name: str


# class Job(BaseModel):
#     id: str = Field(..., alias="_id")
#     title: str
#     requirements: List[str]
#     description: str
#     # position: Optional[str] = None
#     # jobType: Optional[str] = None
#     # salary: Optional[str] = None
#     # createdAt: Optional[str] = None
#     company: Company


# class MatchRequest(BaseModel):
#     resume_url: str
#     jobs: List[Job]


# @app.post("/match-jobs")
# def match_jobs(request: MatchRequest):
#     matched = match_resume_to_jobs(request.resume_url, [job.dict() for job in request.jobs])
#     return {"matched_jobs": matched}



from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime # Import datetime for date parsing
from resume_matcher import match_resume_to_jobs

# Assuming match_resume_to_jobs is in a separate file or defined below this.
# from resume_matcher import match_resume_to_jobs

app = FastAPI()

# Company schema as per your Node.js payload, assuming it's what's pulled from MongoDB
# Make sure your Company Mongoose schema matches what you populate here.
class Company(BaseModel):
    # If your company is directly embedded, you might not have an _id for it in the payload.
    # But since you are populating 'company', it will have its own _id.
    # However, your current Node.js payload only sends 'name' and 'logo' for company.
    # If you need the company _id in the payload, you'd have to include it in the Node.js map.
    # For now, let's stick to what's in your current JS payload.
    name: str
    logo: Optional[str] = None # Assuming 'logo' is a field you might pull for company

class Job(BaseModel):
    # Mapped from Mongoose's _id
    id: str = Field(..., alias="_id")

    title: str
    description: str
    requirements: List[str]

    # Changed type to float as salary is Number in Mongoose
    salary: float

    # Added new fields from Mongoose schema
    experienceLevel: int # Mongoose Number maps to Python int/float
    location: str

    jobType: str
    # Changed type to int as position is Number in Mongoose
    position: int

    # Mongoose ObjectId references are just the ID string in the payload
    # Your Node.js code sends only company name/logo, not the ObjectId.
    # So, keep this as a nested Pydantic model.
    company: Company

    # createdAt from Mongoose timestamps is a Date object, sent as ISO string.
    # It's always present due to timestamps:true, but making it Optional[datetime]
    # is safer if your Node.js select doesn't explicitly include it, though it should.
    createdAt: Optional[datetime] = None

    # Note: `created_by` and `applications` are not in your current Node.js `select`
    # for `jobs`, so they should NOT be in your Pydantic model if you're not sending them.
    # If you later decide to send them, add them as:
    # created_by: Optional[str] = None # For ObjectId string
    # applications: Optional[List[str]] = None # For array of ObjectId strings

class MatchRequest(BaseModel):
    resume_url: str
    jobs: List[Job]

@app.post("/match-jobs")
def match_jobs(request: MatchRequest):
    # Ensure your `match_resume_to_jobs` function is correctly imported or defined.
    # When you pass `job.model_dump(by_alias=True)`, it converts the Pydantic Job model
    # back into a dictionary, using '_id' for the 'id' field, which matches the expected
    # input structure if your `match_resume_to_jobs` function relies on `_id`.
    matched = match_resume_to_jobs(request.resume_url, [job.model_dump(by_alias=True) for job in request.jobs])
    return {"matched_jobs": matched}

# ... (rest of your resume_matcher.py or functions if in the same file)