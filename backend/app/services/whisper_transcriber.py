# backend/app/services/whisper_transcriber.py

import whisper

def transcribe_audio(file_path: str) -> str:
    model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
    result = model.transcribe(file_path)
    return result["text"]

# Local test
if __name__ == "__main__":
    file_path = "/Users/AnnaM10vir/ai-resume-coach/IMG_1049.mp4"  # ✅ Replace with your video/audio file path
    transcript = transcribe_audio(file_path)
    print("📝 Transcription Result:\n")
    print(transcript)
