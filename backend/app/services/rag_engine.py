# backend/app/services/rag_engine.py

from app.services.search_client import search_documents

def generate_rag_answer(query: str) -> dict:
    docs = search_documents(query)

    context = "\n".join([doc["text"] for doc in docs])
    answer = f"""🧠 GPT-style RAG Answer (Mocked):

Your query: **{query}**

We found {len(docs)} matching documents. Based on them, here's a helpful insight:

"{context}"

(Note: This will be enhanced with GPT-4 once access is granted.)
"""

    return {
        "query": query,
        "documents": docs,
        "answer": answer
    }
