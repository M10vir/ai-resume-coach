import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load from .env
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
SEARCH_API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION", "2021-04-30-Preview")

# 🔍 Search documents (used in /search and /rag-search)
def search_documents(query: str, top_k: int = 3):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version={SEARCH_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    payload = {
        "search": query,
        "top": top_k
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    results = response.json()
    return results.get("value", [])


# ⬆️ Upload a document to Azure Search (used in /upload-resume)
def upload_document_to_search(document: dict):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/index?api-version={SEARCH_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    payload = {
        "value": [{ **document, "@search.action": "upload" }]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code >= 400:
        print("❌ Failed to upload document:", response.text)
        response.raise_for_status()
