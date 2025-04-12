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

def generate_rag_answer(query: str) -> dict:
    docs = search_documents(query)

    # ✅ Truncate each document's text to avoid token overflow (1000 chars max)
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
