import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import download_file, extract_text_from_pdf

WORD_RE = re.compile(r"[a-zA-Z0-9+#\.]+")

def tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in WORD_RE.findall(text)}

def cosine_and_coverage(resume_txt: str, job_req_tokens: set[str]) -> tuple[float, float]:
    documents = [resume_txt.lower(), " ".join(job_req_tokens)]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    cosine = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]) * 100

    resume_tokens = tokenize(resume_txt)
    coverage = 0.0
    if job_req_tokens:
        matched = resume_tokens & job_req_tokens
        coverage = len(matched) / len(job_req_tokens) * 100

    return round(cosine, 2), round(coverage, 2)

def match_resume_to_jobs(resume_url: str, jobs: list[dict]) -> list[dict]:
    # Use the shared utility functions
    resume_file = download_file(resume_url)
    resume_text = extract_text_from_pdf(resume_file)

    results = []
    for job in jobs:
        # Clean up the requirements list
        cleaned_requirements = []
        for req_str in job.get("requirements", []):
            for r in req_str.split(','):
                cleaned_requirements.append(r.strip().replace('"', ''))
        
        req_tokens = tokenize(" ".join(cleaned_requirements))
        cosine, coverage = cosine_and_coverage(resume_text, req_tokens)

        job_copy = job.copy()
        job_copy["cosine_score"] = cosine
        job_copy["skill_coverage"] = coverage
        results.append(job_copy)

    # Sort by coverage first, then cosine
    return sorted(results, key=lambda j: (j["skill_coverage"], j["cosine_score"]), reverse=True)