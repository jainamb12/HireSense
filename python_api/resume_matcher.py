import re
import requests 
from io import BytesIO
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WORD_RE = re.compile(r"[a-zA-Z0-9+#\.]+")

def download_resume(resume_url: str) -> BytesIO:
    r = requests.get(resume_url, timeout=10)
    r.raise_for_status()
    return BytesIO(r.content)

def extract_resume_text(file_obj: BytesIO) -> str:
    return extract_text(file_obj)

# ---------- NEW helper ----------
def tokenize(text: str) -> set[str]:
    return {tok.lower() for tok in WORD_RE.findall(text)}

def cosine_and_coverage(resume_txt: str, job_req_tokens: set[str]) -> tuple[float, float]:
    # --- cosine ---
    documents = [resume_txt.lower(), " ".join(job_req_tokens)]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    cosine = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]) * 100  # 0‑100

    # --- coverage ---
    resume_tokens = tokenize(resume_txt)
    if not job_req_tokens:
        coverage = 0.0
    else:
        matched = resume_tokens & job_req_tokens
        coverage = len(matched) / len(job_req_tokens) * 100  # 0‑100

    return round(cosine, 2), round(coverage, 2)

# ---------- MAIN entry ----------
# def match_resume_to_jobs(resume_url: str, jobs: list[dict]) -> list[dict]:
#     resume_file = download_resume(resume_url)
#     resume_text = extract_resume_text(resume_file)

#     results = []
#     for job in jobs:
#         req_tokens = tokenize(" ".join(job["requirements"]))
#         cosine, coverage = cosine_and_coverage(resume_text, req_tokens)

#         job_copy = {k: job.get(k) for k in ("id", "title", "requirements", "description", "company")}
#         job_copy["cosine_score"] = cosine            # 0‑100 based on full text
#         job_copy["skill_coverage"] = coverage        # 0‑100 based on req list
#         results.append(job_copy)

#     # sort by coverage first, then cosine
#     return sorted(results, key=lambda j: (j["skill_coverage"], j["cosine_score"]), reverse=True)

# ... (imports and helper functions)

# ---------- MAIN entry ----------
def match_resume_to_jobs(resume_url: str, jobs: list[dict]) -> list[dict]:
    resume_file = download_resume(resume_url)
    resume_text = extract_resume_text(resume_file)

    results = []
    for job in jobs:
        # Ensure job["requirements"] is a list of strings, not a single string with quotes inside
        # The current requirements: ["\"React JS\", ..."] will be treated as one long string.
        # It should be ["React JS", "JavaScript", ...]
        # This is likely coming from your MongoDB storage. You might need to fix how requirements are stored
        # or parse them here. For now, let's assume they *should* be a list of individual strings.
        # If your database stores it as a single string like "skill1, skill2, skill3",
        # you'll need to split it:
        # req_tokens = tokenize(" ".join(job["requirements"]).replace('"', '').split(', '))

        # Given your current output, requirements is a list of a single string.
        # Let's assume your tokenizing function can handle this, but it's not ideal.
        # For now, let's just make sure the `job` dictionary passed to `tokenize`
        # has correctly structured requirements.

        # Safest way to handle requirements: ensure they are iterated over.
        # If requirements is `["\"React JS\", \"JavaScript\""]`, then `join` makes it one string.
        # If it's `["React JS", "JavaScript"]`, it also works fine.
        # The key is to remove the inner quotes during processing if they are part of the string.
        # Let's clean up the requirements if they contain extra quotes
        cleaned_requirements = []
        for req_str in job["requirements"]:
            # This handles cases like `["\"React JS\", \"JavaScript\", ..."]` by splitting and cleaning
            # Or just `["React JS"]`
            for r in req_str.split(','):
                cleaned_requirements.append(r.strip().replace('"', '')) # Remove leading/trailing space and quotes

        req_tokens = tokenize(" ".join(cleaned_requirements))


        cosine, coverage = cosine_and_coverage(resume_text, req_tokens)

        # Create a copy of the *entire* job dictionary received from FastAPI
        # Then add the new scores. This preserves all original fields.
        job_copy = job.copy() # Make a shallow copy of the job dict

        # Add the calculated scores
        job_copy["cosine_score"] = cosine
        job_copy["skill_coverage"] = coverage

        results.append(job_copy)

    # sort by coverage first, then cosine
    return sorted(results, key=lambda j: (j["skill_coverage"], j["cosine_score"]), reverse=True)
