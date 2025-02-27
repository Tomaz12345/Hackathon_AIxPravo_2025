import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CheckerPage from './pages/CheckerPage';
import ResultPage from './pages/ResultPage';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Navbar className="fixed top-0 left-0 w-full z-50"/>
        <main className="flex-grow overflow-auto pt-16 pb-16">
          <Routes>
            <Route path='/' element={<HomePage />} />
            <Route path="/checker" element={<CheckerPage />} />
            <Route path="/result/:id" element={<ResultPage />} />
          </Routes>
        </main>
        <Footer className="fixed top-0 left-0 w-full z-50"/>
      </div>
    </Router>
  );
}

export default App;
