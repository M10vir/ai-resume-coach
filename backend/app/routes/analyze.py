# backend/app/routes/analyze.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.openai_client import analyze_resume

router = APIRouter()

class ResumeInput(BaseModel):
    text: str

@router.post("/analyze-resume")
def analyze_resume_route(resume: ResumeInput):
    try:
        feedback = analyze_resume(resume.text)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
