import React from 'react';
import { ShieldCheck, Database, Compass, Clock, Activity, CheckSquare } from 'lucide-react';

export const About: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight mb-2">
          About TerraSeek
        </h1>
        <p className="text-sm text-slate-600">
          A satellite-imagery search and change-analysis platform built on the philosophy:
          <strong className="text-slate-900 ml-1">SEARCH → FIND → VERIFY → UNDERSTAND</strong>
        </p>
      </div>

      <div className="space-y-6 text-xs text-slate-700 leading-relaxed">
        {/* Core Principles */}
        <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-base font-bold text-slate-900">Truth-in-AI Commitment</h2>
          <p>
            TerraSeek rejects fabricated ML confidence scores. In high-stakes remote sensing intelligence (disaster response, infrastructure monitoring, environmental compliance), image similarity alone is never treated as proof.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div className="p-3 bg-green-50/70 border border-green-200 rounded">
              <span className="font-bold text-green-900 block mb-1">SUPPORTED</span>
              Target candidate exists, mandatory spatial proximity constraints are mathematically satisfied, temporal baseline continuity is proven, and change features are confirmed.
            </div>
            <div className="p-3 bg-amber-50/70 border border-amber-200 rounded">
              <span className="font-bold text-amber-900 block mb-1">NEEDS_REVIEW</span>
              Evidence exists but spectral contrast is near threshold, observation gap is wide, or proximity is borderline. Automatically escalated to human review.
            </div>
            <div className="p-3 bg-slate-100 border border-slate-300 rounded">
              <span className="font-bold text-slate-900 block mb-1">INSUFFICIENT_EVIDENCE</span>
              Baseline historical imagery is missing or sensor observations are corrupted. Missing evidence is never converted into a false negative conclusion.
            </div>
            <div className="p-3 bg-rose-50/70 border border-rose-200 rounded">
              <span className="font-bold text-rose-900 block mb-1">NO_MATCH</span>
              Target entity is absent from the catalog, or strict spatial boundaries are violated. No fabricated candidates are created.
            </div>
          </div>
        </div>

        {/* Architecture */}
        <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm space-y-3">
          <h2 className="text-base font-bold text-slate-900">System Architecture</h2>
          <p>
            TerraSeek integrates modern geospatial standards:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-600">
            <li><strong>PostgreSQL + PostGIS:</strong> Spatially indexed feature layers and geodesic topology analysis.</li>
            <li><strong>Qdrant Vector Database:</strong> Semantic candidate retrieval supporting GeoRSCLIP foundation embeddings.</li>
            <li><strong>Rasterio & NumPy:</strong> High-performance multi-spectral array computation (NDVI vegetation indices, MNDWI water delineation).</li>
            <li><strong>Mission Compiler:</strong> Inspectable natural language parser translating analyst intent into strict spatial/temporal execution plans.</li>
            <li><strong>FastAPI & React:</strong> Full-stack typed architecture with zero external tile dependencies in offline mode.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
