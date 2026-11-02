import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def analyze_resume(resume_text, job_description):
    skills = [
        "Python", "Java", "C++", "SQL", "HTML",
        "CSS", "JavaScript", "React", "Machine Learning",
        "Data Analysis", "Communication", "Problem Solving"
    ]

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    found_skills = [
        skill for skill in skills
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", resume_lower)
    ]

    required_skills = [
        skill for skill in skills
        if re.search(r"\b" + re.escape(skill.lower()) + r"\b", job_lower)
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([
        resume_text, job_description
    ])

    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100

    return found_skills, missing_skills, round(score, 2)