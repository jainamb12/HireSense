import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def download_resume(resume_url):
    response = requests.get(resume_url)
    response.raise_for_status()
    return BytesIO(response.content)


def extract_resume_text(resume_file):
    return extract_text(resume_file)


def calculate_match_score(resume_text, job):
    job_requirements = " ".join(job["requirements"]).lower()
    documents = [resume_text.lower(), job_requirements]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return float(similarity[0][0])  # Convert numpy float to Python float


def match_resume_to_jobs(resume_url, jobs):
    resume_file = download_resume(resume_url)
    resume_text = extract_resume_text(resume_file)
    
    results = []
    for job in jobs:
        score = calculate_match_score(resume_text, job)
        job_with_score = job.copy()
        job_with_score["match_score"] = round(score * 100, 2)
        results.append(job_with_score)

    # Sort jobs by score descending
    return sorted(results, key=lambda x: x["match_score"], reverse=True)
