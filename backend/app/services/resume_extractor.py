# backend/app/services/resume_extractor.py

from pdfminer.high_level import extract_text as extract_pdf
from docx import Document

def extract_text_from_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""
