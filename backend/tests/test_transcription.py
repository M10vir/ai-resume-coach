# backend/tests/test_transcription.py

from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_transcribe_audio_route():
    test_audio_path = "backend/tests/test_audio.wav"
    assert os.path.exists(test_audio_path), "❌ Test audio file not found!"

    with open(test_audio_path, "rb") as audio_file:
        response = client.post(
            "/transcribe-audio",
            files={"file": ("test_audio.wav", audio_file, "audio/wav")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data and isinstance(data["transcript"], str)
    assert "gpt_feedback" in data and isinstance(data["gpt_feedback"], str)
