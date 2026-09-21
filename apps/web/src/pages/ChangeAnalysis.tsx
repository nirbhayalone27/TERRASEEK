import React, { useState } from 'react';
import { changeApi } from '../api/client';
import { ChangeType } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Eye, Layers, CheckSquare, Activity, Calendar } from 'lucide-react';

export const ChangeAnalysis: React.FC = () => {
  const [siteId, setSiteId] = useState('site-01');
  const [changeTypes, setChangeTypes] = useState<ChangeType[]>(['BUILDING']);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const availableTypes: ChangeType[] = ['BUILDING', 'ROAD', 'VEGETATION', 'WATER'];

  const toggleType = (t: ChangeType) => {
    if (changeTypes.includes(t)) {
      if (changeTypes.length > 1) {
        setChangeTypes(changeTypes.filter((x) => x !== t));
      }
    } else {
      setChangeTypes([...changeTypes, t]);
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await changeApi.analyze(siteId, undefined, undefined, changeTypes);
      setResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Automated Change Extraction</h1>
        <p className="text-xs text-slate-500">
          Execute multi-domain change detection pipeline (Structural differences, NDVI vegetation loss, MNDWI water contours).
        </p>
      </div>

      <div className="bg-white p-5 rounded-lg border border-slate-200 mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Target Site</label>
            <select
              value={siteId}
              onChange={(e) => setSiteId(e.target.value)}
              className="w-full text-xs bg-slate-50 border border-slate-300 rounded p-2"
            >
              <option value="site-01">Site 01 - Riverside Development</option>
              <option value="site-02">Site 02 - Industrial Expansion</option>
              <option value="site-03">Site 03 - Highway Bypass</option>
              <option value="site-04">Site 04 - Forest Canopy Loss</option>
              <option value="site-05">Site 05 - Alps Reservoir Extent</option>
            </select>
          </div>

          <div className="sm:col-span-2">
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Select Change Features to Delineate
            </label>
            <div className="flex gap-2 flex-wrap">
              {availableTypes.map((t) => {
                const active = changeTypes.includes(t);
                return (
                  <button
                    key={t}
                    type="button"
                    onClick={() => toggleType(t)}
                    className={`px-3 py-1.5 rounded text-xs font-semibold border transition-colors ${
                      active
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-slate-50 text-slate-700 border-slate-300 hover:bg-slate-100'
                    }`}
                  >
                    {t}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="px-4 py-2 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors flex items-center gap-1.5 shadow-sm"
        >
          <Activity className="w-3.5 h-3.5" />
          {loading ? 'Running Detection Pipeline...' : 'Run Pipeline & Extract Features'}
        </button>
      </div>

      {result && (
        <div className="bg-white p-5 rounded-lg border border-slate-200">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Change Extraction Results</h3>
              <p className="text-xs text-slate-500">Observation window: {result.earlier_date} → {result.later_date}</p>
            </div>
            <StatusBadge status={result.status} size="md" />
          </div>

          <p className="text-xs text-slate-700 mb-4">{result.summary}</p>

          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wide">
              Extracted Change Polygons ({result.changes?.length || 0})
            </h4>

            {result.changes?.map((c: any) => (
              <div key={c.id} className="p-3 bg-slate-50 rounded border border-slate-200 text-xs">
                <div className="flex items-center justify-between font-semibold text-slate-800 mb-1">
                  <span>{c.change_type} Footprint Delineated</span>
                  <StatusBadge status={c.status} size="sm" />
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-slate-600">
                  <div>
                    <span className="text-slate-400 block">Area:</span>
                    <span className="font-medium text-slate-800">{c.area_sq_meters} m²</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Model:</span>
                    <span className="font-medium text-slate-800">{c.model_name}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Model Tier:</span>
                    <span className="font-mono text-slate-800">{c.model_tier}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Verified:</span>
                    <span className="font-medium text-green-700">Supported</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
