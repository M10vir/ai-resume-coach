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
      setError('🚨 Failed to fetch results. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <h2 style={{ fontSize: '1.6rem', marginBottom: '1rem' }}>🔍 AI Resume Coach - RAG Search</h2>

      <input
        type="text"
        placeholder="Enter your query (e.g. Python developer)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        style={{
          width: '100%',
          padding: '1rem',
          fontSize: '1rem',
          marginBottom: '1rem',
          border: '1px solid #333',
          borderRadius: '4px',
          background: '#1e1e1e',
          color: '#fff'
        }}
      />

      <button
        onClick={handleSearch}
        disabled={loading}
        style={{
          padding: '0.75rem 2rem',
          backgroundColor: '#1f1f1f',
          border: 'none',
          color: '#fff',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        {loading ? 'Searching...' : 'Search'}
      </button>

      {error && (
        <div style={{ marginTop: '1rem', color: 'tomato' }}>
          {error}
        </div>
      )}

      {answer && (
        <div style={{ marginTop: '2rem' }}>
          <h3>🧠 RAG Answer</h3>
          <pre style={{
            background: '#2c2c2c',
            padding: '1rem',
            borderRadius: '4px',
            color: '#d4d4d4'
          }}>{answer.answer}</pre>

          <h4 style={{ marginTop: '1.5rem' }}>📄 Source Documents</h4>
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
