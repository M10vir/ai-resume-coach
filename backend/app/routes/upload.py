from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from uuid import uuid4
from app.services.resume_extractor import extract_text_from_resume
from app.services.search_client import upload_document_to_search

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    resume_id = str(uuid4())
    file_ext = file.filename.split('.')[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{resume_id}.{file_ext}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_resume(file_path)

    if not text.strip():
        raise HTTPException(status_code=422, detail="Failed to extract text from resume")

    upload_document_to_search({
        "id": resume_id,
        "name": file.filename,
        "summary": "Uploaded resume",
        "skills": [],
        "text": text
    })

    return { "message": "Resume uploaded and indexed", "resume_id": resume_id }
