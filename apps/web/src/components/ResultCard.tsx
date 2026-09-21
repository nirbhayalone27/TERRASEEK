import React from 'react';
import { Link } from 'react-router-dom';
import { SearchResultItem } from '../types';
import { StatusBadge } from './StatusBadge';
import { MapPin, Calendar, ArrowRight, ShieldCheck } from 'lucide-react';

interface Props {
  result: SearchResultItem;
  isSelected?: boolean;
  onSelect?: () => void;
}

export const ResultCard: React.FC<Props> = ({ result, isSelected = false, onSelect }) => {
  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-lg border transition-all cursor-pointer ${
        isSelected
          ? 'bg-blue-50/40 border-blue-500 shadow-sm'
          : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-sm'
      }`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <span className="text-xs font-semibold text-blue-700 tracking-wide uppercase">
            {result.change_type} CHANGE
          </span>
          <h3 className="text-sm font-bold text-slate-900 leading-snug">{result.site_name}</h3>
        </div>
        <StatusBadge status={result.status} size="sm" />
      </div>

      <div className="space-y-1.5 text-xs text-slate-600 mb-3">
        <div className="flex items-center gap-1.5">
          <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span className="truncate">{result.location_name}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
          <span>{result.earlier_date} → {result.later_date}</span>
        </div>
      </div>

      <div className="bg-slate-50 p-2 rounded border border-slate-100 text-xs text-slate-700 mb-3">
        <div className="flex items-center gap-1 font-medium text-slate-800 mb-0.5">
          <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
          <span>Evidence Summary</span>
        </div>
        <p className="line-clamp-2 text-slate-600">{result.evidence_summary}</p>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
        <span className="text-xs text-slate-400 font-mono">ID: {result.site_id}</span>
        <Link
          to={`/sites/${result.site_id}`}
          className="text-xs font-semibold text-blue-700 hover:text-blue-900 flex items-center gap-1"
          onClick={(e) => e.stopPropagation()}
        >
          <span>Investigate Site</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
