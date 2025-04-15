// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RAGSearch from './pages/RAGSearch';
import ResumeManager from './pages/ResumeManager'; // ✅ Add this line

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/rag-search" element={<RAGSearch />} />
        <Route path="/resumes" element={<ResumeManager />} />  {/* ✅ This line must exist */}
        <Route path="/" element={
          <>
            <h1>🏠 Welcome to AI Resume Coach</h1>
            <p>Use the <a href="/rag-search">RAG Search</a> or <a href="/resumes">Resume Manager</a> to explore.</p>
          </>
        } />
      </Routes>
    </Router>
  );
}

export default App;
