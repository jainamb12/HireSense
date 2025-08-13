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
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby", "go", "golang",
    "swift", "objective-c", "php", "r", "rust", "kotlin", "scala", "perl", "matlab",
    "bash", "shell scripting", "powershell",

    # Frontend
    "html", "css", "sass", "less", "tailwind css", "bootstrap", "jquery",
    "react", "reactjs", "react.js", "nextjs", "next.js", "vue", "vuejs", "vue.js",
    "angular", "angularjs", "angular.js", "nuxtjs", "nuxt.js", "ember.js", "svelte",

    # Backend
    "nodejs", "node", "express", "nestjs", "spring", "spring boot",
    "django", "flask", "fastapi", "ruby on rails", ".net", "asp.net",
    "laravel", "codeigniter", "symfony",

    # Databases
    "mysql", "postgres", "postgresql", "mongo", "mongodb", "sqlite",
    "oracle", "cassandra", "redis", "dynamodb", "mariadb", "elasticsearch",
    "firebase", "neo4j", "couchdb", "snowflake", "bigquery",

    # Cloud
    "aws", "amazon web services", "azure", "microsoft azure",
    "gcp", "google cloud platform", "heroku", "digitalocean", "cloudflare",
    "cloudformation", "terraform", "serverless", "lambda", "ec2", "s3",

    # DevOps & Tools
    "docker", "kubernetes", "jenkins", "git", "github", "gitlab", "bitbucket",
    "ci/cd", "ansible", "puppet", "vagrant", "grafana", "prometheus",
    "datadog", "splunk", "sonarqube", "nexus",

    # Data Science / ML / AI
    "machine learning", "ml", "deep learning", "dl", "artificial intelligence", "ai",
    "data science", "data analysis", "nlp", "natural language processing",
    "computer vision", "cv", "reinforcement learning",
    "pandas", "numpy", "matplotlib", "seaborn",
    "scikit-learn", "tensorflow", "tf", "pytorch", "pyt",
    "keras", "huggingface", "transformers",
    "powerbi", "tableau", "data visualization", "plotly",
    "big data", "spark", "hadoop", "hive", "pig",

    # Security
    "cybersecurity", "network security", "firewall", "penetration testing",
    "vulnerability assessment", "encryption", "cryptography",
    "incident response", "malware analysis", "siem",

    # APIs
    "rest", "restful apis", "graphql", "postman", "swagger", "openapi",

    # Project Management & Collaboration
    "jira", "confluence", "trello", "slack",
    "agile", "scrum", "kanban",

    # Soft Skills (often in JDs)
    "communication", "teamwork", "problem-solving", "critical thinking",
    "leadership", "adaptability", "collaboration", "time management",
    "project management", "attention to detail", "mentoring", "negotiation",
    "presentation"
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