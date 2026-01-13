from flask import Flask, request, render_template
from resume_parser import extract_text_from_pdf, clean_text, extract_skills, extract_phrases
from job_matcher import analyze_job_description, match_skills
from skills import SKILLS
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files["resume"]
        jd_text = request.form["job_description"]

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
    app.run()

