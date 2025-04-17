# backend/app/services/rag_engine.py

import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.services.search_client import search_documents
from datetime import datetime

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# 📁 Create logs directory
os.makedirs("logs", exist_ok=True)

def log_gpt_call(prompt_type: str, user_prompt: str, response: str = "", error: str = ""):
    with open("logs/gpt_api.log", "a") as log_file:
        log_file.write(f"\n==== {prompt_type} | {datetime.utcnow()} ====\n")
        log_file.write(f"🧠 Prompt:\n{user_prompt}\n")
        if response:
            log_file.write(f"\n✅ Response:\n{response}\n")
        if error:
            log_file.write(f"\n❌ Error:\n{error}\n")


def safe_gpt_call(system_prompt: str, user_prompt: str, prompt_type: str = "general") -> str:
    """Helper to safely call GPT with retry on rate limits and log the interaction."""
    try:
        print("[AI] Calling GPT-4o...")
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        message = response.choices[0].message.content
        log_gpt_call(prompt_type, user_prompt, response=message)
        return message
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            print("[AI] Rate limit hit. Retrying after 60 seconds...")
            time.sleep(60)
            try:
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                message = response.choices[0].message.content
                log_gpt_call(prompt_type, user_prompt, response=message)
                return message
            except Exception as retry_e:
                log_gpt_call(prompt_type, user_prompt, error=str(retry_e))
                return f"(GPT-4 feedback unavailable due to error: {retry_e})"
        log_gpt_call(prompt_type, user_prompt, error=error_msg)
        return f"(GPT-4 feedback unavailable due to error: {error_msg})"


# 🔍 Used by RAG Search
def generate_rag_answer(query: str) -> dict:
    docs = search_documents(query)
    context = "\n".join([doc["text"][:1000] for doc in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    system_prompt = "You're an AI Resume Coach. Use the context below to answer the question."

    answer = safe_gpt_call(system_prompt, prompt, prompt_type="rag-search")

    return {
        "query": query,
        "documents": docs,
        "answer": answer
    }


# 🧠 Used by upload to auto-analyze a resume
def generate_gpt_feedback(resume_text: str) -> str:
    prompt = f"Resume:\n{resume_text[:4000]}"
    system_prompt = "You're a professional resume coach. Provide constructive feedback to improve the resume text."
    return safe_gpt_call(system_prompt, prompt, prompt_type="resume-feedback")


def analyze_resume_with_gpt(resume_text: str) -> str:
    prompt = f"""
You are a senior resume reviewer and career coach. Carefully read the resume content below and provide a helpful analysis including:

- Summary of the candidate's strengths
- Suggestions for improvement (e.g., formatting, clarity, skills)
- Any gaps or areas that could be highlighted more
- Optional: Advice on tailoring the resume for a specific job role

Resume Content:
\"\"\"
{resume_text[:3500]}
\"\"\"
"""
    system_prompt = "You're a helpful assistant providing professional resume feedback."
    return safe_gpt_call(system_prompt, prompt, prompt_type="detailed-analysis")

# 🧠 Create Helper: analyze_transcript_with_gpt()

def analyze_transcript_with_gpt(transcript: str) -> str:
    prompt = f"""
You're an expert communication coach. Analyze the following transcript from a mock interview or speech and provide feedback on:

- Clarity and coherence of speech
- Use of filler words or repetition
- Professional tone and delivery
- Suggestions for improvement

Transcript:
\"\"\"
{transcript[:3500]}
\"\"\"
"""
    system_prompt = "You're a communication coach giving constructive feedback."
    return safe_gpt_call(system_prompt, prompt)
