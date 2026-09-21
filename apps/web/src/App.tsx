import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/Header';
import { Home } from './pages/Home';
import { Search } from './pages/Search';
import { FindSimilar } from './pages/FindSimilar';
import { Compare } from './pages/Compare';
import { ChangeAnalysis } from './pages/ChangeAnalysis';
import { SiteDetail } from './pages/SiteDetail';
import { EvidenceDetail } from './pages/EvidenceDetail';
import { ReviewQueue } from './pages/ReviewQueue';
import { JobDetail } from './pages/JobDetail';
import { ReportDetail } from './pages/ReportDetail';
import { About } from './pages/About';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Search />} />
            <Route path="/similar" element={<FindSimilar />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/change" element={<ChangeAnalysis />} />
            <Route path="/sites/:siteId" element={<SiteDetail />} />
            <Route path="/evidence/:evidenceId" element={<EvidenceDetail />} />
            <Route path="/review" element={<ReviewQueue />} />
            <Route path="/jobs/:jobId" element={<JobDetail />} />
            <Route path="/reports/:reportId" element={<ReportDetail />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
          TerraSeek — Satellite Imagery Search & Change-Analysis Platform &copy; 2026. Offline-First Architecture.
        </footer>
      </div>
    </Router>
  );
};
export default App;
