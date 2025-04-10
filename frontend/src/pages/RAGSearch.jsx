import React, { useState } from 'react';
import { fetchRagAnswer } from '../services/ragService';

const RAGSearch = () => {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setAnswer(null);

    try {
      const result = await fetchRagAnswer(query);
      setAnswer(result);
    } catch (err) {
      setError('Failed to fetch results.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '0 auto', padding: '2rem' }}>
      <h2>🔍 AI Resume Coach - RAG Search</h2>
      <input
        type="text"
        placeholder="Enter your query (e.g. Python developer)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: '100%', padding: '0.75rem', fontSize: '1rem' }}
      />
      <button onClick={handleSearch} style={{ marginTop: '1rem', padding: '0.75rem 1.5rem' }}>
        Search
      </button>

      {loading && <p>Loading RAG answer...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {answer && (
        <div style={{ marginTop: '2rem' }}>
          <h3>🧠 RAG Answer</h3>
          <pre>{answer.answer}</pre>

          <h4>📄 Source Documents</h4>
          <ul>
            {answer.documents.map((doc) => (
              <li key={doc.id}>
                <strong>{doc.name}</strong>: {doc.summary}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RAGSearch;
