# backend/app/services/emotion_detector.py

from pyannote.audio import Pipeline
import os

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Lazy-load the pipeline to avoid global state issues
_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = Pipeline.from_pretrained("pyannote/embedding", use_auth_token=HF_TOKEN)
    return _pipeline

def detect_emotion(audio_file_path: str) -> str:
    """
    Run emotion detection pipeline (placeholder).

    Args:
        audio_file_path (str): Path to an audio or video file.

    Returns:
        str: Predicted emotion (currently a dummy).
    """
    pipeline = get_pipeline()
    embedding = pipeline(audio_file_path)

    # Placeholder: You would run classification here
    return "🟡 Neutral (demo - real classification needs fine-tuning)"
