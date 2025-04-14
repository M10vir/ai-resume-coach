import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load from .env
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")
SEARCH_API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION", "2021-04-30-Preview")

# 🔍Search documents (used in /search and /rag-search)
def search_documents(query: str, top_k: int = 2):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version={SEARCH_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    payload = {
        "search": query,
        "top": top_k,
        "select": "id,name,text,summary"  # Only fetch necessary fields
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        results = response.json()
        return results.get("value", [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Azure Cognitive Search error: {e}")
        return []

# ⬆️Upload a document to Azure Search (used in /upload-resume)
def upload_document_to_search(document: dict):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/index?api-version={SEARCH_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    payload = {
        "value": [{ **document, "@search.action": "upload" }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("❌ Failed to upload document to Azure Search:", e)
