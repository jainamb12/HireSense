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
    resume_file = download_file(resume_url)
    resume_text = extract_text_from_pdf(resume_file)
    resume_tokens = tokenize(resume_text)
    # 1. Prepare all documents
    job_texts = []
    job_req_tokens_list = []
    for job in jobs:
        reqs = [r.strip().replace('"', '') for req_str in job.get("requirements", []) for r in req_str.split(',')]
        job_texts.append(" ".join(reqs))
        job_req_tokens_list.append(tokenize(" ".join(reqs)))

    all_docs = [resume_text.lower()] + job_texts

    # 2. Vectorize all at once
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(all_docs)
    resume_vector = tfidf_matrix[0:1]
    jobs_vectors = tfidf_matrix[1:]

    # 3. Calculate all cosine similarities
    cosine_scores = cosine_similarity(resume_vector, jobs_vectors)[0]

    results = []
    for i, job in enumerate(jobs):
        # Calculate coverage
        job_req_tokens = job_req_tokens_list[i]
        coverage = 0.0
        if job_req_tokens:
            matched = resume_tokens & job_req_tokens
            coverage = len(matched) / len(job_req_tokens) * 100

        job_copy = job.copy()
        job_copy["cosine_score"] = round(float(cosine_scores[i]) * 100, 2) # Get pre-calculated score
        job_copy["skill_coverage"] = round(coverage, 2)
        results.append(job_copy)

    return sorted(results, key=lambda j: (j["skill_coverage"], j["cosine_score"]), reverse=True)