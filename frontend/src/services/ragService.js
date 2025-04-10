export async function fetchRagAnswer(query) {
  const response = await fetch(`http://localhost:8000/rag-search?q=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error("Failed to fetch RAG answer");
  }
  return await response.json();
}
