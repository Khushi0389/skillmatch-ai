from fastapi import FastAPI, UploadFile, File, Form
from app.resume_parser import parse_pdf, parse_docx
from app.extractor import extract_skills
from app.matcher import calculate_match

app = FastAPI()

@app.post("/analyze/")
async def analyze_resume(file: UploadFile = File(...), jd: str = Form(...)):
    ext = file.filename.split(".")[-1]
    contents = await file.read()
    path = f"temp.{ext}"
    with open(path, "wb") as f:
        f.write(contents)

    text = parse_pdf(path) if ext == "pdf" else parse_docx(path)
    skills = extract_skills(text)
    match_score = calculate_match(text, jd)

    return {"skills": skills, "match_score": match_score}
