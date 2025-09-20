# HireSense - AI-Powered Job Portal 🚀

<p align="center">
  <i>An intelligent job portal that uses AI to match candidates with their dream jobs and provides detailed, actionable feedback to improve their resumes.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React Badge"/>
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js Badge"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Badge"/>
  <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB Badge"/>
</p>

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏗️ Architecture](#️-architecture)
- [🚀 Getting Started](#-getting-started)
- [🔮 Future Work](#-future-work)
- [👤 Author](#-author)

---

## 📖 Project Overview

HireSense is a modern, full-stack job portal designed to bridge the gap between talented candidates and their ideal career opportunities. Unlike traditional job boards that rely on simple keyword matching, HireSense leverages a sophisticated, hybrid AI engine to understand the context and meaning behind both a candidate's resume and a job description. This results in more accurate job recommendations, while also providing users with personalized, data-driven feedback to enhance their resumes and improve their chances of success.

---

## ✨ Key Features

-   **🧠 AI-Powered Job Recommendations:** Utilizes a hybrid engine blending keyword precision (TF-IDF) and semantic understanding (Sentence-Transformers) for highly accurate job ranking.
-   **📄 Explainable AI Resume Analysis:** Generates a detailed report with a precise `Overall Fit Score`, a prioritized list of "Must-Have" vs. "Good-to-Have" missing skills, and smart, actionable suggestions for improvement.
-   **📊 Data Analytics Dashboard:** Provides visualizations of job market trends, including top in-demand skills, salary distributions by location, and job type distributions.
-   **👤 Full User & Application Management:** Complete CRUD functionality for user authentication, profile management (including resume uploads), and job applications.

---

## 🛠️ Tech Stack

-   **Frontend:** React, Vite, Redux Toolkit, Tailwind CSS, Shadcn UI
-   **Backend (Main):** Node.js, Express.js
-   **AI Microservice:** Python, FastAPI, Pydantic
-   **Database:** MongoDB
-   **AI/ML Libraries:** Sentence-Transformers, PyTorch, Scikit-learn, spaCy, Pandas
-   **Utilities:** `pdfminer.six` (for resume parsing)

---

## 🏗️ Architecture

HireSense is built on a modern **microservice architecture** to ensure scalability and separation of concerns.



-   The **main application** is a standard MERN stack (MongoDB, Express.js, React, Node.js) that handles all user interactions, authentication, and core application logic.
-   For computationally intensive and specialized tasks, the Node.js backend makes API calls to a dedicated **Python/FastAPI microservice**, which serves as the "brain" for all AI-powered features.

---

## 🚀 Getting Started

### Prerequisites
-   Node.js (v22 or later)
-   Python (v3.11 or later)
-   A MongoDB Atlas connection string

### Local Setup
1.  Clone the repository:
    ```bash
    git clone [https://github.com/jainamb12/HireSense](https://github.com/jainamb12/HireSense)
    cd job portal
    ```
2.  **Setup the Backend & Frontend:**
    * In two separate terminals, navigate to the `backend` and `frontend` directories and run `npm install`.
    * Create a `.env` file in each directory and populate it with the required variables (e.g., `MONGO_URI`, `VITE_API_URL`).
3.  **Setup the Python API:**
    * Navigate to the `python_api` directory.
    * Create and activate a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate # On Windows: .\venv\Scripts\activate
        ```
    * Install dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    * Create a `.env` file with your `MONGO_DETAILS` and other variables.
4.  **Run the Application:**
    * Terminal 1 (in `frontend`): `npm run dev`
    * Terminal 2 (in `backend`): `npm run dev`
    * Terminal 3 (in `python_api`): `uvicorn main:app --reload`

---

## 🔮 Future Work

-   [ ] **Salary Prediction:** Train a model to predict a realistic salary range for a job based on its description and requirements.
-   [ ] **Career Path Recommender:** Suggest potential next career steps and skills to learn based on a user's resume.
-   [ ] **NER for Structured Data:** Enhance the analysis engine to extract years of experience per skill using Named Entity Recognition.

---

## 👤 Author

**Jainam Bhavsar**
-   **GitHub:** [@jainamb12](https://github.com/jainamb12)
-   **LinkedIn:** [linkedin.com/in/jainam-bhavsar-lj](https://linkedin.com/in/jainam-bhavsar-lj)