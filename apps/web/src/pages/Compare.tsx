import React, { useState } from 'react';
import { BeforeAfterViewer } from '../components/BeforeAfterViewer';
import { changeApi } from '../api/client';
import { GitCompare, Calendar, ShieldCheck, Activity } from 'lucide-react';

export const Compare: React.FC = () => {
  const [selectedSite, setSelectedSite] = useState<string>('site-01');
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const demoSites = [
    { id: 'site-01', name: 'Site 01 - Riverside Development (Buildings)' },
    { id: 'site-02', name: 'Site 02 - Industrial Logistics Expansion (Construction)' },
    { id: 'site-03', name: 'Site 03 - Highway Bypass Construction (Road)' },
    { id: 'site-04', name: 'Site 04 - Forest Canopy Loss (Vegetation)' },
    { id: 'site-05', name: 'Site 05 - Reservoir Surface Extent (Water)' },
  ];

  const handleRunComparison = async () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('site_id', selectedSite);

    try {
      const res = await changeApi.compare(formData);
      setSummary(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Compare Satellite Observations</h1>
          <p className="text-xs text-slate-500">
            Multi-temporal visual and analytical comparison across historical passes.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedSite}
            onChange={(e) => setSelectedSite(e.target.value)}
            className="text-xs bg-white border border-slate-300 rounded px-3 py-2 font-medium text-slate-800"
          >
            {demoSites.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>

          <button
            onClick={handleRunComparison}
            disabled={loading}
            className="px-4 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded text-xs font-medium transition-colors flex items-center gap-1.5 shadow-sm"
          >
            <GitCompare className="w-3.5 h-3.5" />
            {loading ? 'Evaluating...' : 'Run Analytical Compare'}
          </button>
        </div>
      </div>

      {summary && (
        <div className="mb-6 p-4 bg-white rounded-lg border border-slate-200 text-xs">
          <div className="flex items-center justify-between pb-2 border-b border-slate-100 mb-2">
            <div className="flex items-center gap-1.5 font-bold text-slate-800">
              <Activity className="w-4 h-4 text-blue-700" />
              <span>Analytical Delta Analysis</span>
            </div>
            <span className="font-mono text-[11px] px-2 py-0.5 bg-slate-100 rounded text-slate-600">
              Model: {summary.model_name} ({summary.model_tier})
            </span>
          </div>
          <p className="text-slate-700 mb-2">{summary.summary}</p>
          {summary.spectral_summary && (
            <div className="flex gap-4 text-slate-600 font-mono text-[11px]">
              {Object.entries(summary.spectral_summary).map(([k, v]) => (
                <span key={k}>
                  {k}: <strong>{String(v)}</strong>
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      <BeforeAfterViewer siteId={selectedSite} />
    </div>
  );
};
