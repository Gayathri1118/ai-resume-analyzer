from skills import SKILLS, SKILL_ALIASES
from resume_parser import clean_text, extract_skills, extract_phrases

IMPORTANT_SKILLS = {"python", "machine learning", "nlp"}


def analyze_job_description(jd_text):
    clean = clean_text(jd_text)
    tokens = extract_skills(clean, SKILLS)
    phrases = extract_phrases(clean, SKILLS)
    return set(tokens + phrases)


def normalize_skills(skills):
    normalized = set(skills)

    for main, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if alias in skills:
                normalized.add(main)

    return normalized


def match_skills(resume_skills, jd_skills):
    resume_skills = normalize_skills(resume_skills)
    jd_skills = normalize_skills(jd_skills)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    score = 0
    total_weight = 0

    for skill in jd_skills:
        weight = 2 if skill in IMPORTANT_SKILLS else 1
        total_weight += weight
        if skill in resume_skills:
            score += weight

    final_score = round((score / total_weight) * 100, 2) if total_weight else 0

    return {
        "score": final_score,
        "matched": sorted(matched),
        "missing": sorted(missing)
    }
