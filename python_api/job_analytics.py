import pandas as pd
from typing import Dict, Any, List, Optional
from utils import job_collection, TECH_SKILLS

def get_job_analytics_data(
    location: Optional[str] = 'all',
    job_type: Optional[str] = 'all'
) -> Dict[str, Any]:
    try:
        query_filter = {}
        if location and location != 'all':
            query_filter['location'] = location
        if job_type and job_type != 'all':
            query_filter['jobType'] = job_type

        jobs_cursor = job_collection.find(query_filter, {'_id': 0})
        jobs = list(jobs_cursor)
        
        if not jobs:
            return {
                "top_skills": [],
                "job_type_distribution": [],
                "avg_salary_by_location": [],
                "unique_locations": [],
                "unique_job_types": []
            }
        
        df = pd.DataFrame(jobs)
        df['jobType'] = df['jobType'].str.lower()
        df['location'] = df['location'].str.lower()
        # 1. Top 10 In-Demand Skills
        all_skills = []
        for req_list in df['requirements']:
            for req_str in req_list:
                cleaned_requirements = [r.strip().replace('"', '') for r in req_str.split(',')]
                # Filter skills to only include those in your TECH_SKILLS list for consistency
                all_skills.extend([s for s in cleaned_requirements if s in TECH_SKILLS])
        
        skill_counts = pd.Series(all_skills).value_counts().head(10).to_dict()
        top_skills_data = [{"skill": skill, "count": int(count)} for skill, count in skill_counts.items()]

        # 2. Job Type Distribution
        job_type_counts = df['jobType'].value_counts().to_dict()
        job_type_distribution_data = [{"job_type": job_type, "count": int(count)} for job_type, count in job_type_counts.items()]

        # 3. Average Salary by Location
        avg_salary_by_location_data = df.groupby('location')['salary'].mean().round(2).to_dict()
        avg_salary_by_location_list = [{"location": loc, "avg_salary": sal} for loc, sal in avg_salary_by_location_data.items()]

        # Unique filter options for the frontend
        unique_locations_list = sorted(df['location'].unique().tolist())
        unique_job_types_list = sorted(df['jobType'].unique().tolist())
        
        return {
            "top_skills": top_skills_data,
            "job_type_distribution": job_type_distribution_data,
            "avg_salary_by_location": avg_salary_by_location_list,
            "unique_locations": unique_locations_list,
            "unique_job_types": unique_job_types_list
        }
    
    except Exception as e:
        # Re-raise the exception to be caught by the FastAPI endpoint's error handler
        raise Exception(f"An error occurred while processing analytics: {e}")