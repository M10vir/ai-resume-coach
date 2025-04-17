# backend/app/routes/transcribe.py

from fastapi import UploadFile, File, APIRouter, HTTPException
from app.services.whisper_transcriber import transcribe_audio
from app.services.rag_engine import analyze_transcript_with_gpt

router = APIRouter()

@router.post("/transcribe-audio")
async def transcribe_audio_route(file: UploadFile = File(...)):
    print(f"📦 Incoming file content_type: {file.content_type}")

    allowed_types = [
        "audio/wav", "audio/x-wav", "audio/wave",
        "audio/mpeg", "audio/mp3", "audio/x-m4a", "audio/webm",
        "application/octet-stream"  # ✅ Generic uploads
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()
    temp_file_path = "temp_audio.wav"
    with open(temp_file_path, "wb") as f:
        f.write(contents)

    # 🧠 Transcribe
    transcript = transcribe_audio(temp_file_path)

    # 💬 Analyze with GPT-4
    gpt_feedback = analyze_transcript_with_gpt(transcript)

    return {
        "transcript": transcript,
        "gpt_feedback": gpt_feedback
    }
