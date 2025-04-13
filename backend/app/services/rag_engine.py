import os
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

# 🔍 Used by RAG Search
def generate_rag_answer(query: str) -> dict:
    docs = search_documents(query)

    # ✅ Truncate each document's text to avoid token overflow
    context = "\n".join([doc["text"][:1000] for doc in docs])

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You're an AI Resume Coach. Use the context below to answer the question."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}"
                }
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"❌ Error calling GPT-4o:\n\n{str(e)}"

    return {
        "query": query,
        "documents": docs,
        "answer": answer
    }

# 🧠 Used by upload to auto-analyze a resume
def analyze_resume_with_gpt(resume_text: str) -> str:
    """Analyze resume text and return GPT-4 feedback."""
    prompt = f"""
You are a senior resume reviewer and career coach. Carefully read the resume content below and provide a helpful analysis including:

- Summary of the candidate's strengths
- Suggestions for improvement (e.g., formatting, clarity, skills)
- Any gaps or areas that could be highlighted more
- Optional: Advice on tailoring the resume for a specific job role

Resume Content:
\"\"\"
{resume_text[:3500]}  # ✂️ GPT-4o safe token truncation
\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                { "role": "system", "content": "You're a helpful assistant providing professional resume feedback." },
                { "role": "user", "content": prompt }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"(GPT-4 feedback failed)\n\n{str(e)}"
