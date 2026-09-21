import React from 'react';
import { EvidenceStatus } from '../types';
import { CheckCircle2, AlertTriangle, HelpCircle, XCircle } from 'lucide-react';

interface Props {
  status: EvidenceStatus | string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<Props> = ({ status, size = 'md' }) => {
  const s = status.toUpperCase();

  let bg = 'bg-slate-100 text-slate-700 border-slate-300';
  let Icon = HelpCircle;
  let label = 'Unknown';

  if (s === 'SUPPORTED') {
    bg = 'bg-green-50 text-green-800 border-green-200';
    Icon = CheckCircle2;
    label = 'Supported';
  } else if (s === 'NEEDS_REVIEW') {
    bg = 'bg-amber-50 text-amber-800 border-amber-200';
    Icon = AlertTriangle;
    label = 'Needs Review';
  } else if (s === 'INSUFFICIENT_EVIDENCE') {
    bg = 'bg-slate-100 text-slate-700 border-slate-300';
    Icon = HelpCircle;
    label = 'Insufficient Evidence';
  } else if (s === 'NO_MATCH') {
    bg = 'bg-rose-50 text-rose-800 border-rose-200';
    Icon = XCircle;
    label = 'No Match';
  }

  const padding = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-xs';

  return (
    <span className={`inline-flex items-center gap-1.5 font-medium border rounded-md ${padding} ${bg}`}>
      <Icon className={size === 'sm' ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
      {label}
    </span>
  );
};
