import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { searchApi } from '../api/client';
import { SearchResponse, SearchResultItem } from '../types';
import { SearchBox } from '../components/SearchBox';
import { ResultCard } from '../components/ResultCard';
import { MapView } from '../components/MapView';
import { StatusBadge } from '../components/StatusBadge';
import { ShieldCheck, Info, Compass, AlertCircle } from 'lucide-react';

export const Search: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || 'new buildings near a river';

  const [currentQuery, setCurrentQuery] = useState(queryParam);
  const [response, setResponse] = useState<SearchResponse | null>(null);
  const [selectedResult, setSelectedResult] = useState<SearchResultItem | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runSearch = async (query: string) => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setSearchParams({ q: query });
    setCurrentQuery(query);

    try {
      const data = await searchApi.search(query);
      setResponse(data);
      if (data.results && data.results.length > 0) {
        setSelectedResult(data.results[0]);
      } else {
        setSelectedResult(null);
      }
    } catch (err: any) {
      setError(err.message || 'Search execution failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSearch(queryParam);
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Search Header */}
      <div className="mb-6 bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
        <SearchBox initialQuery={currentQuery} onSearch={runSearch} isLoading={loading} />
      </div>

      {/* Error Banner */}
      {error && (
        <div className="mb-6 p-4 bg-rose-50 border border-rose-200 rounded-lg text-rose-800 text-sm flex items-center gap-2">
          <AlertCircle className="w-5 h-5 shrink-0 text-rose-600" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Analysis Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Results List and Mission Inspection (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {/* Execution Plan & Intent Box */}
          {response && (
            <div className="bg-white p-4 rounded-lg border border-slate-200 text-xs">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100 mb-2">
                <div className="flex items-center gap-1.5 font-bold text-slate-800">
                  <Compass className="w-4 h-4 text-blue-700" />
                  <span>Mission Compiler Plan</span>
                </div>
                <StatusBadge status={response.status} size="sm" />
              </div>
              <ul className="space-y-1 text-slate-600">
                {response.execution_plan.map((step, idx) => (
                  <li key={idx} className="flex items-start gap-1.5">
                    <span className="text-blue-600 font-bold">•</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Results Header */}
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-600">
              Results Found ({response?.total_results ?? 0})
            </span>
            {response && <span className="text-xs text-slate-500">{response.summary}</span>}
          </div>

          {/* Results List */}
          {loading ? (
            <div className="p-8 text-center text-xs text-slate-500 bg-white rounded-lg border border-slate-200">
              Running spatial, temporal, and change verification pipeline...
            </div>
          ) : response?.results && response.results.length > 0 ? (
            <div className="space-y-3">
              {response.results.map((r) => (
                <ResultCard
                  key={r.site_id}
                  result={r}
                  isSelected={selectedResult?.site_id === r.site_id}
                  onSelect={() => setSelectedResult(r)}
                />
              ))}
            </div>
          ) : (
            <div className="p-8 text-center bg-white rounded-lg border border-slate-200">
              <Info className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              <h4 className="text-sm font-bold text-slate-800 mb-1">
                {response?.status === 'NO_MATCH' ? 'No Matching Candidates' : 'No Results'}
              </h4>
              <p className="text-xs text-slate-500 max-w-sm mx-auto">
                {response?.summary || 'Try adjusting your spatial or temporal search query.'}
              </p>
            </div>
          )}
        </div>

        {/* Right: Map View (7 cols) */}
        <div className="lg:col-span-7 h-[620px] sticky top-20">
          <MapView
            results={response?.results || []}
            selectedResult={selectedResult}
            onSelectSite={(site) => setSelectedResult(site)}
          />
        </div>
      </div>
    </div>
  );
};
