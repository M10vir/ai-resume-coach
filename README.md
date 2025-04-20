
## AI-Powered Resume & Interview Coach

This project is a full-stack AI application that leverages Azure OpenAI, Whisper, FastAPI, PostgreSQL, and Cognitive Search to analyze resumes, transcribe and evaluate interview audio/video, and provide intelligent feedback using LLM and RAG techniques.

# Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Environment Configuration](#environment-configuration)
- [Setup Instructions](#setup-instructions)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Running Tests](#running-tests)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [Showcase Scenarios](#showcase-scenarios)
- [Future Enhancements](#future-enhancements)
- [Author](#author)

# Features

- Upload and analyze resumes (DOCX/PDF)
- GPT-4-powered resume feedback
- Resume search using Azure Cognitive Search with RAG
- Upload and transcribe interview audio/video using Whisper
- GPT-4 feedback on transcripts
- Emotion detection placeholder with `pyannote.audio`
- Frontend with React and Vite
- GitHub Actions pipeline for backend CI

# Architecture Overview

- Azure Blob Storage: Stores uploaded resumes and audio files
- Azure OpenAI (GPT-4): Generates feedback for resumes and interviews
- Azure Cognitive Search: Enables RAG-based query search on indexed resumes
- FastAPI Backend: Handles APIs, file processing, and AI integration
- PostgreSQL: Stores extracted text and AI feedback
- Whisper: Transcribes audio/video
- Frontend (React): Allows resume/audio upload and displays feedback

# Tech Stack

- Frontend: React (Vite)
- Backend: FastAPI, Python 3.11
- AI Models: Azure OpenAI GPT-4, Whisper, pyannote.audio
- Cloud: Azure Blob Storage, Azure Cognitive Search, Azure PostgreSQL
- CI/CD: GitHub Actions
- Testing: Pytest

# Project Structure

```
ai-resume-coach/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── analyze.py
│   │   │   ├── upload.py
│   │   │   ├── transcribe.py
│   │   │   └── resumes.py
│   │   ├── services/
│   │   │   ├── resume_extractor.py
│   │   │   ├── rag_engine.py
│   │   │   ├── whisper_transcriber.py
│   │   │   └── emotion_detector.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_audio.wav
│   │   ├── test_transcription.py
│   │   └── test_emotion_detector.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── ResumeManager.jsx
│   │   │   ├── RAGSearch.jsx
│   │   │   └── TranscriptionPage.jsx
│   │   ├── components/
│   │   └── App.jsx
│   ├── public/
│   ├── index.html
│   └── vite.config.js
│
├── .github/workflows/
│   └── backend-ci.yml
└── README.md
```

# Environment Configuration

Create a `.env` file inside the `backend/` directory with:

```
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_COG_SEARCH_KEY=<your-key>
AZURE_COG_SEARCH_ENDPOINT=<your-endpoint>
AZURE_COG_SEARCH_INDEX_NAME=resumes-index
AZURE_STORAGE_CONNECTION_STRING=<your-blob-connection>
AZURE_STORAGE_CONTAINER_NAME=<your-container>
POSTGRES_URL=postgresql+psycopg2://<username>:<password>@<host>:5432/<db>
HUGGINGFACE_TOKEN=<your-hf-token>
```

# Setup Instructions

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

# Running Tests

```bash
# From root or backend/
PYTHONPATH=. pytest tests/
```

# GitHub Actions CI/CD

Located at `.github/workflows/backend-ci.yml`, the pipeline performs:

- Dependency installation
- Linting and formatting (if enabled)
- Test execution
- Future: Deploy hooks or build artifacts

# Showcase Scenarios

- Upload a resume and get AI feedback on structure, clarity, and strengths
- Use the search feature to query indexed resumes for skills like "Azure DevOps"
- Upload an interview video/audio and receive transcript + GPT feedback
- Emotion detection placeholder provides scope for further enhancement

# Future Enhancements

- Fine-tune emotion classification with pyannote embeddings
- Add video UI timeline visualization
- Enable real-time feedback during video recording
- Dark/light theme toggle in UI
- Export feedback reports (PDF)

# Author

Mohammed Tanvir

Senior AI Engineer | DevOps | Cloud-Native Architect | Hackathon 2024 
GitHub: [M10vir](https://github.com/M10vir)  
Project: AI Resume & Interview Coach

---

This project was built as a submission for the Microsoft Azure AI Hackathon 2025 to demonstrate real-world usage of Azure OpenAI and multimodal AI systems.

