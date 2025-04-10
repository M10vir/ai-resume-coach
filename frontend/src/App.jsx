import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RAGSearch from './pages/RAGSearch';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/rag-search" element={<RAGSearch />} />
        <Route path="/" element={
          <>
            <h1>🏠 Welcome to AI Resume Coach</h1>
            <p>Use the <a href="/rag-search">/rag-search</a> route to test the RAG search experience.</p>
          </>
        } />
      </Routes>
    </Router>
  );
}

export default App;
