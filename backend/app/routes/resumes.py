# backend/app/routes/resumes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Resume

router = APIRouter()

@router.get("/resumes")
def list_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).order_by(Resume.uploaded_at.desc()).all()
    return resumes
