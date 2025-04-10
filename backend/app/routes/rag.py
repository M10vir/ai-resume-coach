# backend/app/routes/rag.py

from fastapi import APIRouter, Query, HTTPException
from app.services.rag_engine import generate_rag_answer

router = APIRouter()

@router.get("/rag-search")
def rag_search(q: str = Query(..., description="Query for RAG-enhanced search")):
    try:
        return generate_rag_answer(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
