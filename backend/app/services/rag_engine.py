# backend/app/services/rag_engine.py

import os import ChatCompletion
from dotenv import load_dotenv
from app.services.search_client import search_documents

# If GPT-4 is ready, uncomment this block
# import openai
# load_dotenv()
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_type = "azure"
# openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
# DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def generate_rag_answer(query: str, mock: bool = True) -> dict:
    docs = search_documents(query)
    context = "\n".join([doc.get("text", "") for doc in docs])

    if not docs:
        return {
            "query": query,
            "documents": [],
            "answer": "🛑 No matching documents found in the search index."
        }

    if mock:
        # Return mock GPT-style RAG answer
        answer = f"""🧠 GPT-style RAG Answer (Mocked):

Your query: **{query}**

We found {len(docs)} matching documents. Based on them, here's a helpful insight:

\"\"\"{context}\"\"\"

(Note: This will be enhanced with GPT-4 once access is granted.)
"""
    else:
        # Uncomment this section when GPT-4 is ready
        # response = openai.ChatCompletion.create(
        #     engine=DEPLOYMENT_NAME,
        #     messages=[
        #         {"role": "system", "content": "You are a helpful AI Resume & Interview Coach."},
        #         {"role": "user", "content": f"Based on the following documents:\n\n{context}\n\nAnswer this question: {query}"}
        #     ],
        #     temperature=0.7,
        #     max_tokens=600
        # )
        # answer = response.choices[0].message["content"]
        answer = "⚠️ GPT-4 integration placeholder. Uncomment code when access is approved."

    return {
        "query": query,
        "documents": docs,
        "answer": answer
    }
