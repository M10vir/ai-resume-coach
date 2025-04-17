from fastapi import UploadFile, File, APIRouter, HTTPException
from app.services.whisper_transcriber import transcribe_audio

router = APIRouter()

@router.post("/transcribe-audio")
async def transcribe_audio_route(file: UploadFile = File(...)):
    print(f"📦 Incoming file content_type: {file.content_type}")  # Add this line to debug

    allowed_types = [
    "audio/wav", "audio/x-wav", "audio/wave",
    "audio/mpeg", "audio/mp3", "audio/x-m4a", "audio/webm",
    "application/octet-stream"  # ✅ Add this to allow generic .wav uploads
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    contents = await file.read()
    with open("temp_audio.wav", "wb") as f:
        f.write(contents)

    transcript = transcribe_audio("temp_audio.wav")
    return {"transcript": transcript}
