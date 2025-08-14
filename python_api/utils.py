import spacy
import requests
from io import BytesIO
from pdfminer.high_level import extract_text
from pymongo import MongoClient
from config import settings

# --- Shared Resources: SpaCy Model and Skills List ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

SKILL_CATEGORIES = {
    "technical": {
        "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby", "go", "golang",
        "swift", "objective-c", "php", "r", "rust", "kotlin", "scala", "perl", "matlab",
        "html", "css", "sass", "less", "tailwind css", "bootstrap", "jquery",
        "react", "reactjs", "react.js", "nextjs", "next.js", "vue", "vuejs", "vue.js",
        "angular", "angularjs", "angular.js", "nuxtjs", "nuxt.js", "ember.js", "svelte",
        "nodejs", "node", "express", "nestjs", "spring", "spring boot",
        "django", "flask", "fastapi", "ruby on rails", ".net", "asp.net",
        "laravel", "codeigniter", "symfony",
        "mysql", "postgres", "postgresql", "mongo", "mongodb", "sqlite",
        "oracle", "cassandra", "redis", "dynamodb", "mariadb", "elasticsearch",
        "firebase", "neo4j", "couchdb", "snowflake", "bigquery",
        "aws", "amazon web services", "azure", "microsoft azure",
        "gcp", "google cloud platform", "heroku", "digitalocean", "cloudflare",
        "cloudformation", "terraform", "serverless", "lambda", "ec2", "s3",
        "machine learning", "ml", "deep learning", "dl", "artificial intelligence", "ai",
        "data science", "data analysis", "nlp", "natural language processing",
        "computer vision", "cv", "reinforcement learning",
        "pandas", "numpy", "matplotlib", "seaborn",
        "scikit-learn", "tensorflow", "tf", "pytorch", "pyt",
        "keras", "huggingface", "transformers",
        "big data", "spark", "hadoop", "hive", "pig",
        "cybersecurity", "network security", "firewall", "penetration testing",
        "vulnerability assessment", "encryption", "cryptography",
        "incident response", "malware analysis", "siem",
        "rest", "restful apis", "graphql"
    },
    "tools": {
        "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "bitbucket",
        "ci/cd", "ansible", "puppet", "vagrant", "grafana", "prometheus",
        "datadog", "splunk", "sonarqube", "nexus",
        "powerbi", "tableau", "data visualization", "plotly",
        "postman", "swagger", "openapi",
        "jira", "confluence", "trello", "slack",
        "bash", "shell scripting", "powershell"
    },
    "soft_skills": {
        "agile", "scrum", "kanban",
        "communication", "teamwork", "problem-solving", "critical thinking",
        "leadership", "adaptability", "collaboration", "time management",
        "project management", "attention to detail", "mentoring", "negotiation",
        "presentation"
    }
}

def get_all_skills() -> set:
    """Combines all skills from all categories into a single set."""
    all_skills = set()
    for category in SKILL_CATEGORIES.values():
        all_skills.update(category)
    return all_skills

# This is our master list of all skills, used for extraction
ALL_SKILLS = get_all_skills()
SINGLE_WORD_SKILLS = {s for s in ALL_SKILLS if " " not in s}
MULTI_WORD_SKILLS = {s for s in ALL_SKILLS if " " in s}

# --- MongoDB Client Setup ---
client = MongoClient(settings.mongo_details)
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
    
def load_resume_text(url: str) -> str:
    """Downloads a resume PDF from URL and returns extracted text."""
    file_obj = download_file(url)
    return extract_text_from_pdf(file_obj)