import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    raw_text = extract_text_from_pdf("sample_resumes/sample.pdf")
    clean = clean_text(raw_text)

    print(clean[:1000])

import spacy
nlp = spacy.load("en_core_web_sm")

def extract_skills(text, skills_list):
    doc = nlp(text)
    found_skills = set()

    for token in doc:
        token_text = token.lemma_.lower()
        for skill in skills_list:
            if token_text == skill:
                found_skills.add(skill)

    return list(found_skills)

def extract_phrases(text, skills_list):
    found = set()
    for skill in skills_list:
        if skill in text:
            found.add(skill)
    return list(found)

if __name__ == "__main__":
    from skills import SKILLS

    raw = extract_text_from_pdf("sample_resumes/sample.pdf")
    clean = clean_text(raw)

    tokens = extract_skills(clean, SKILLS)
    phrases = extract_phrases(clean, SKILLS)

    final_skills = set(tokens + phrases)
    print("Extracted Skills:", final_skills)

