import spacy
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from pymongo import MongoClient
import os

# --- Shared Resources: SpaCy Model and Skills List ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

TECH_SKILLS = {
    "python", "javascript", "typescript", "java", "c#", "c++", "ruby", "go",
    "swift", "php", "html", "css", "sql", "r", "rust", "kotlin", "perl", "golang",
    "c", "matlab", "react", "angular", "vue", "django", "flask", "express",
    "nodejs", "node", "next.js", "nuxt.js", "nest.js", "spring", "spring boot",
    "ruby on rails", ".net", "asp.net", "tailwind css", "bootstrap", "jquery",
    "sass", "less", "aws", "amazon web services", "azure", "microsoft azure",
    "gcp", "google cloud platform", "docker", "kubernetes", "jenkins", "gitlab",
    "terraform", "ansible", "ci/cd", "devops", "cloud computing", "lambda", "ec2",
    "s3", "azure devops", "mongodb", "mongo", "mysql", "postgresql", "postgres",
    "sql server", "sqlite", "oracle", "cassandra", "redis", "firebase",
    "machine learning", "ai", "artificial intelligence", "data science", "nlp",
    "natural language processing", "deep learning", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "data visualization", "powerbi", "tableau", "spark",
    "hadoop", "cybersecurity", "network security", "firewall", "encryption",
    "cryptography", "malware analysis", "penetration testing", "incident response",
    "vulnerability assessment", "forensics", "siem", "security information and event management",
    "git", "github", "gitlab", "jira", "agile", "scrum", "kanban", "restful apis",
    "rest", "api", "microservices", "unit testing", "tdd", "documentation", "graphql",
    "postman", "oauth", "jira", "confluence", "communication", "teamwork",
    "problem-solving", "critical thinking", "adaptability", "leadership",
    "collaboration", "time management", "project management", "attention to detail",
    "creative", "analytical",
}

# --- MongoDB Client Setup ---
client = MongoClient("mongodb+srv://jainam121005:0ds1WTpR1V7qZeBy@cluster0.1zstuon.mongodb.net/")
db = client['test']
job_collection = db['jobs']

# --- Shared Utility Functions ---
def download_file(url: str) -> BytesIO:
    """Downloads a file from a URL and returns it as a BytesIO object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.RequestException as e:
        raise ValueError(f"Failed to download file from {url}: {e}")

def extract_text_from_pdf(file_obj: BytesIO) -> str:
    """Extracts text from a PDF file object."""
    try:
        return extract_text(file_obj)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")