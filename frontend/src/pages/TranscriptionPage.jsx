// frontend/src/pages/TranscriptionPage.jsx

import React, { useState } from "react";
import axios from "axios";

const TranscriptionPage = () => {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [gptFeedback, setGptFeedback] = useState("");
  const [emotion, setEmotion] = useState(""); // 🆕 Emotion State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setTranscript("");
    setGptFeedback("");
    setEmotion(""); // 🆕 Reset emotion
    setError("");
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/transcribe-audio", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTranscript(response.data.transcript);
      setGptFeedback(response.data.gpt_feedback);
      setEmotion(response.data.emotion || "Not detected"); // 🆕 Set emotion
    } catch (err) {
      console.error(err);
      setError("❌ Upload or transcription failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto", color: "white" }}>
      <h2>🎤 Audio/Video Transcription</h2>

      {/* Upload Form */}
      <input
        type="file"
        accept="audio/*,video/*"
        onChange={handleFileChange}
        style={{ marginRight: "1rem" }}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Transcribing..." : "Upload & Transcribe"}
      </button>

      {/* Error Message */}
      {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}

      {/* Transcript */}
      {transcript && (
        <>
          <h3 style={{ marginTop: "2rem" }}>📝 Transcript</h3>
          <pre style={{ backgroundColor: "#1e1e1e", padding: "1rem", borderRadius: "5px" }}>
            {transcript}
          </pre>
        </>
      )}

      {/* GPT Feedback */}
      {gptFeedback && (
        <>
          <h3 style={{ marginTop: "2rem" }}>💡 GPT Feedback</h3>
          <pre style={{ backgroundColor: "#1e1e1e", padding: "1rem", borderRadius: "5px" }}>
            {gptFeedback}
          </pre>
        </>
      )}

      {/* Emotion Detection */}
      {emotion && (
        <>
          <h3 style={{ marginTop: "2rem" }}>🎭 Detected Emotion</h3>
          <p style={{ fontSize: "1.1rem" }}>{emotion}</p>
        </>
      )}
    </div>
  );
};

export default TranscriptionPage;
