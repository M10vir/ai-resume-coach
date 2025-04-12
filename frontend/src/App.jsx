import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RAGSearch from './pages/RAGSearch';
import ResumeManager from './pages/ResumeManager'; // ✅ NEW IMPORT

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/rag-search" element={<RAGSearch />} />
        <Route path="/resume-manager" element={<ResumeManager />} /> {/* ✅ NEW ROUTE */}
        <Route path="/" element={
          <>
            <h1>🏠 Welcome to AI Resume Coach</h1>
            <p>Use the <a href="/rag-search">/rag-search</a> or <a href="/resume-manager">/resume-manager</a> routes.</p> {/* ✅ Updated text */}
          </>
        } />
      </Routes>
    </Router>
  );
}

export default App;
