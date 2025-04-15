import React, { useState, useEffect } from "react";
import axios from "axios";

const ResumeManager = () => {
  console.log("✅ ResumeManager component mounted"); // for debug

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setSuccess("");
    setError("");
  };

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/resumes");
      setResumes(response.data);
    } catch (err) {
      setError("❌ Failed to load resumes. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setSuccess("");
    setError("");
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setFile(null);
      setSuccess("✅ Resume uploaded successfully!");
      fetchResumes(); // refresh list
    } catch (err) {
      setError("❌ Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  return (
    <div style={{
      maxWidth: "900px",
      margin: "2rem auto",
      padding: "2rem",
      backgroundColor: "#111827",
      color: "white",
      border: "1px solid #ccc",
      borderRadius: "8px"
    }}>
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

      {/* Status Messages */}
      {success && <p style={{ color: "lightgreen" }}>{success}</p>}
      {error && (
        <p style={{ color: "red" }}>
          {error}{" "}
          <button onClick={fetchResumes} style={{ marginLeft: "10px" }}>
            🔁 Retry
          </button>
        </p>
      )}

      {/* Resume List */}
      <h3>📄 Uploaded Resumes ({resumes.length})</h3>
      {loading ? (
        <p>⏳ Loading...</p>
      ) : resumes.length === 0 ? (
        <p>No resumes uploaded yet.</p>
      ) : (
        <ul>
          {resumes.map((resume) => (
            <li key={resume.id} style={{ marginBottom: "1.5rem" }}>
              <strong>{resume.filename}</strong> <br />
              <small>
                Uploaded:{" "}
                {resume.uploaded_at
                  ? new Date(resume.uploaded_at).toLocaleString()
                  : "N/A"}
              </small>

              {/* AI Feedback */}
              {resume.ai_feedback && (
                <details style={{ marginTop: "0.5rem" }}>
                  <summary><strong>💡 AI Feedback</strong></summary>
                  <pre style={{ whiteSpace: "pre-wrap", marginTop: "0.5rem" }}>
                    {resume.ai_feedback}
                  </pre>
                </details>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ResumeManager;
