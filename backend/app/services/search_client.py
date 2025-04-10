import os
import requests
from dotenv import load_dotenv

load_dotenv()

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

def search_documents(query: str, top_k: int = 3):
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version=2021-04-30-Preview"

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
