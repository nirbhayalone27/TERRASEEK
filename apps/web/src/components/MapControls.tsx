import React from 'react';
import { Plus, Minus, RotateCcw, Layers } from 'lucide-react';

interface Props {
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
}

export const MapControls: React.FC<Props> = ({ onZoomIn, onZoomOut, onReset }) => {
  return (
    <div className="absolute top-3 right-3 flex flex-col gap-1 z-10 bg-white border border-slate-200 rounded-md shadow-sm overflow-hidden">
      <button
        onClick={onZoomIn}
        title="Zoom In"
        className="p-1.5 hover:bg-slate-100 text-slate-700 transition-colors border-b border-slate-100"
      >
        <Plus className="w-4 h-4" />
      </button>
      <button
        onClick={onZoomOut}
        title="Zoom Out"
        className="p-1.5 hover:bg-slate-100 text-slate-700 transition-colors border-b border-slate-100"
      >
        <Minus className="w-4 h-4" />
      </button>
      <button
        onClick={onReset}
        title="Reset Map View"
        className="p-1.5 hover:bg-slate-100 text-slate-700 transition-colors"
      >
        <RotateCcw className="w-4 h-4" />
      </button>
    </div>
  );
};
