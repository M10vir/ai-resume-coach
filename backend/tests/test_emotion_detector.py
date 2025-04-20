# backend/tests/test_emotion_detector.py

import os
import pytest
from unittest import mock
from app.services import emotion_detector

def test_detect_emotion_mocked():
    # Arrange: Create a dummy audio file
    fake_audio_path = "tests/fake_audio.wav"
    with open(fake_audio_path, "wb") as f:
        f.write(b"\0" * 100)

    # Patch the pipeline used inside emotion_detector
    with mock.patch("app.services.emotion_detector.Pipeline") as MockPipeline:
        mock_pipeline_instance = mock.Mock()
        mock_pipeline_instance.return_value = "mocked_embedding"
        MockPipeline.from_pretrained.return_value = mock_pipeline_instance

        # Inject the mocked pipeline into the module
        emotion_detector._pipeline = mock_pipeline_instance

        # Act
        result = emotion_detector.detect_emotion(fake_audio_path)

        # Assert
        assert "Neutral" in result

    os.remove(fake_audio_path)
