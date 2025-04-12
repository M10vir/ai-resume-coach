import React, { useState, useEffect } from "react";
import axios from "axios";

const ResumeManager = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [resumes, setResumes] = useState([]);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const fetchResumes = async () => {
    try {
      const response = await axios.get("http://localhost:8000/resumes");
      setResumes(response.data);
    } catch (err) {
      setError("Failed to load resumes.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      fetchResumes(); // refresh list
    } catch (err) {
      setError("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto", color: "white" }}>
      <h2>📥 Resume Manager</h2>

      {/* Upload Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          style={{ marginRight: "1rem" }}
        />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
      </form>

      {/* Error */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Resume List */}
      <h3>📄 Uploaded Resumes</h3>
      {resumes.length === 0 ? (
        <p>No resumes uploaded yet.</p>
      ) : (
        <ul>
          {resumes.map((resume) => (
            <li key={resume.id} style={{ marginBottom: "1rem" }}>
              <strong>{resume.filename}</strong> <br />
              <small>Uploaded: {new Date(resume.uploaded_at).toLocaleString()}</small>
              {resume.ai_feedback && (
                <div style={{ marginTop: "0.5rem" }}>
                  <strong>AI Feedback:</strong>
                  <pre>{resume.ai_feedback}</pre>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResumeManager;
