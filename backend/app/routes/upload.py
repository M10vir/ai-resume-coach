from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from uuid import uuid4

from app.services.resume_extractor import extract_text_from_resume
from app.services.search_client import upload_document_to_search
from app.services.rag_engine import analyze_resume_with_gpt

from app.models import Resume
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    resume_id = str(uuid4())
    file_ext = file.filename.split('.')[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{resume_id}.{file_ext}")

    # Save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    extracted_text = extract_text_from_resume(file_path)
    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="Failed to extract text from resume")

    # 🔍 Upload to Azure Search
    upload_document_to_search({
        "id": resume_id,
        "name": file.filename,
        "summary": "Uploaded resume",
        "skills": [],
        "text": extracted_text
    })

    # 🧠 Get GPT-4 feedback
    ai_feedback = analyze_resume_with_gpt(extracted_text)

    # 💾 Save to PostgreSQL
    db: Session = next(get_db())
    db_resume = Resume(
        id=resume_id,
        filename=file.filename,
        file_path=file_path,
        extracted_text=extracted_text,
        ai_feedback=ai_feedback
    )
    db.add(db_resume)
    db.commit()

    return {
        "message": "Resume uploaded, analyzed, and indexed",
        "resume_id": resume_id
    }
