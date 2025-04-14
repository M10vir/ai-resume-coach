# backend/app/services/rag_engine.py

import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
from app.services.search_client import search_documents

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def safe_gpt_call(system_prompt: str, user_prompt: str) -> str:
    """Helper to safely call GPT with retry on rate limits."""
    try:
        print("[AI] Calling GPT-4o...")
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
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
                return response.choices[0].message.content
            except Exception as retry_e:
                return f"(GPT-4 feedback unavailable due to error: {retry_e})"
        return f"(GPT-4 feedback unavailable due to error: {error_msg})"


# 🔍 Used by RAG Search
def generate_rag_answer(query: str) -> dict:
    docs = search_documents(query)

    # ✅ Truncate each document's text to avoid token overflow
    context = "\n".join([doc["text"][:1000] for doc in docs])

    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    system_prompt = "You're an AI Resume Coach. Use the context below to answer the question."

    answer = safe_gpt_call(system_prompt, prompt)

    return {
        "query": query,
        "documents": docs,
        "answer": answer
    }


# 🧠 Used by upload to auto-analyze a resume
def generate_gpt_feedback(resume_text: str) -> str:
    prompt = f"Resume:\n{resume_text[:4000]}"
    system_prompt = "You're a professional resume coach. Provide constructive feedback to improve the resume text."
    return safe_gpt_call(system_prompt, prompt)


# ✨ Optional: More in-depth GPT resume analysis
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
    return safe_gpt_call(system_prompt, prompt)
