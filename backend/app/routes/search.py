from fastapi import APIRouter, Query, HTTPException
from app.services.search_client import search_documents

router = APIRouter()

@router.get("/search")
def search_endpoint(q: str = Query(..., description="Search query text")):
    try:
        results = search_documents(q)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
