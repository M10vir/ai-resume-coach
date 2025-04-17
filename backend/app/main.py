from fastapi import FastAPI
from app.routes import analyze, search, rag, upload, resumes, video_test
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Resume & Interview Coach API")
app.include_router(video_test.router)

# Register the router
app.include_router(analyze.router)
app.include_router(search.router)
app.include_router(rag.router)
app.include_router(upload.router)
app.include_router(resumes.router)

# Allow frontend to call backend
origins = [
    "http://localhost:5173",  # Vite default port
    # Add deployed URL here later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "Backend is healthy 🚀"}
