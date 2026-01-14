from flask import Flask, request, render_template
from resume_parser import extract_text_from_pdf, clean_text, extract_skills, extract_phrases
from job_matcher import analyze_job_description, match_skills
from skills import SKILLS
import spacy
import os

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

nlp = spacy.load("en_core_web_sm")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files.get("resume")
        jd_text = request.form.get("job_description", "")

        if not resume:
            return render_template("index.html", error="No resume uploaded")

        resume_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
        resume.save(resume_path)

        raw = extract_text_from_pdf(resume_path)
        clean = clean_text(raw)

        resume_skills = set(
            extract_skills(clean, SKILLS) +
            extract_phrases(clean, SKILLS)
        )

        jd_skills = analyze_job_description(jd_text)
        result = match_skills(resume_skills, jd_skills)

        return render_template("index.html", result=result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
