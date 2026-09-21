import React, { useState } from 'react';
import { EvidencePassport, EvidenceItem } from '../types';
import { StatusBadge } from './StatusBadge';
import { ShieldCheck, ChevronDown, ChevronRight, Compass, Clock, Activity, FileText } from 'lucide-react';

interface Props {
  passport: EvidencePassport;
  onSendToReview?: () => void;
}

export const EvidencePanel: React.FC<Props> = ({ passport, onSendToReview }) => {
  const [expandedIds, setExpandedIds] = useState<Record<string, boolean>>({});

  const toggleItem = (id: string) => {
    setExpandedIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <div className="bg-white p-5 rounded-lg border border-slate-200">
      <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-200 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <ShieldCheck className="w-5 h-5 text-blue-700" />
            <h3 className="text-base font-bold text-slate-900">Evidence Passport</h3>
          </div>
          <p className="text-xs text-slate-500 font-mono">Query: "{passport.query}"</p>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 block mb-1">Truth Determination</span>
          <StatusBadge status={passport.status} size="md" />
        </div>
      </div>

      {/* Summary Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-5">
        <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 mb-1">
            <Compass className="w-4 h-4 text-blue-600" />
            <span>Spatial Criteria</span>
          </div>
          <p className="text-xs text-slate-600">{passport.spatial_summary}</p>
        </div>

        <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 mb-1">
            <Clock className="w-4 h-4 text-blue-600" />
            <span>Temporal Verification</span>
          </div>
          <p className="text-xs text-slate-600">{passport.temporal_summary}</p>
        </div>

        <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700 mb-1">
            <Activity className="w-4 h-4 text-blue-600" />
            <span>Change Evidence</span>
          </div>
          <p className="text-xs text-slate-600">{passport.change_summary}</p>
        </div>
      </div>

      {/* Itemized Evidence List */}
      <div className="mb-5">
        <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
          Auditable Evidence Items ({passport.items.length})
        </h4>

        <div className="space-y-2">
          {passport.items.map((item) => {
            const isExpanded = !!expandedIds[item.id];
            return (
              <div key={item.id} className="border border-slate-200 rounded-md overflow-hidden bg-slate-50/50">
                <div
                  onClick={() => toggleItem(item.id)}
                  className="p-3 flex items-center justify-between cursor-pointer hover:bg-slate-100/60 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    {isExpanded ? (
                      <ChevronDown className="w-4 h-4 text-slate-500" />
                    ) : (
                      <ChevronRight className="w-4 h-4 text-slate-500" />
                    )}
                    <span className="text-xs font-semibold text-slate-800">
                      [{item.evidence_type}] {item.title}
                    </span>
                  </div>
                  <StatusBadge status={item.status} size="sm" />
                </div>

                {isExpanded && (
                  <div className="px-4 pb-3 pt-1 border-t border-slate-200/60 text-xs text-slate-600 space-y-2 bg-white">
                    <p className="text-slate-800">{item.description}</p>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 bg-slate-50 p-2 rounded border border-slate-100">
                      <div>
                        <span className="text-slate-400 block font-mono">Source:</span>
                        <span className="font-medium text-slate-700">{item.source}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block font-mono">Method:</span>
                        <span className="font-medium text-slate-700">{item.method}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block font-mono">Timestamp:</span>
                        <span className="font-medium text-slate-700">
                          {new Date(item.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Provenance & Limitations */}
      <div className="p-3 rounded-md bg-slate-100 border border-slate-200 text-xs text-slate-600 space-y-1">
        <div className="font-semibold text-slate-800">Model Provenance & Limitations</div>
        <div>
          Adapter:{' '}
          <span className="font-mono text-slate-700">
            {passport.model_provenance?.adapter || 'DemoChangeDetectionAdapter'}
          </span>
        </div>
        <div>
          Limitations:{' '}
          <span className="text-slate-700">
            {passport.limitations?.join('; ') || 'Synthetic demonstration environment.'}
          </span>
        </div>
      </div>
    </div>
  );
};
