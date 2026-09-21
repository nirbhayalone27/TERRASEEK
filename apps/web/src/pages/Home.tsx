import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBox } from '../components/SearchBox';
import { Search, Layers, GitCompare, Eye, ShieldCheck, MapPin, Database } from 'lucide-react';

export const Home: React.FC = () => {
  const navigate = useNavigate();

  const handleSearch = (query: string) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  const quickActions = [
    {
      title: 'Find Something',
      description: 'Search satellite imagery using natural language queries.',
      icon: Search,
      path: '/search',
    },
    {
      title: 'Find Similar',
      description: 'Upload an image and find matching geographical features.',
      icon: Layers,
      path: '/similar',
    },
    {
      title: 'Compare Images',
      description: 'Side-by-side and swipe analysis of multi-temporal observations.',
      icon: GitCompare,
      path: '/compare',
    },
    {
      title: 'What Changed?',
      description: 'Automated spectral and structural change detection pipelines.',
      icon: Eye,
      path: '/change',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 sm:py-20">
      {/* Header Banner */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-700 rounded-full border border-blue-200 text-xs font-semibold mb-4">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Truth-in-AI Remote Sensing Intelligence</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-slate-900 mb-3">
          See Change. Find Answers.
        </h1>
        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto">
          Search satellite imagery and investigate what changed. Every conclusion is backed by auditable spatial and temporal evidence.
        </p>
      </div>

      {/* Primary Search Container */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-12">
        <SearchBox onSearch={handleSearch} />
      </div>

      {/* Secondary Actions */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-12">
        {quickActions.map((action) => {
          const Icon = action.icon;
          return (
            <div
              key={action.title}
              onClick={() => navigate(action.path)}
              className="p-5 bg-white rounded-lg border border-slate-200 hover:border-blue-400 hover:shadow-sm cursor-pointer transition-all flex items-start gap-4"
            >
              <div className="p-2.5 rounded-lg bg-blue-50 text-blue-700 border border-blue-100 shrink-0">
                <Icon className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900 mb-1">{action.title}</h3>
                <p className="text-xs text-slate-600 leading-relaxed">{action.description}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Core Philosophy Footnote */}
      <div className="p-4 bg-slate-100 rounded-lg border border-slate-200 text-xs text-slate-600 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-slate-500" />
          <span>Core Protocol: <strong>SEARCH → FIND → VERIFY → UNDERSTAND</strong></span>
        </div>
        <span className="text-slate-500">Zero Fabricated Confidence</span>
      </div>
    </div>
  );
};
