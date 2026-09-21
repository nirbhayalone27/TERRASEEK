import React, { useState } from 'react';
import { Calendar, Layers, Split, Eye } from 'lucide-react';

interface Props {
  siteId: string;
  earlierDate?: string;
  laterDate?: string;
}

export const BeforeAfterViewer: React.FC<Props> = ({
  siteId,
  earlierDate = 'March 15, 2024',
  laterDate = 'January 20, 2025',
}) => {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [mode, setMode] = useState<'side-by-side' | 'swipe'>('side-by-side');

  const beforeUrl = `/api/v1/sites/${siteId}/thumbnail/before`;
  const afterUrl = `/api/v1/sites/${siteId}/thumbnail/after`;

  return (
    <div className="bg-white p-5 rounded-lg border border-slate-200">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-900">Before & After Imagery Verification</h4>
          <p className="text-xs text-slate-500">Optical satellite observation passes (10m Resolution)</p>
        </div>

        <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-md border border-slate-200 text-xs">
          <button
            onClick={() => setMode('side-by-side')}
            className={`px-2.5 py-1 rounded font-medium transition-colors ${
              mode === 'side-by-side' ? 'bg-white shadow-sm text-blue-700' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Side by Side
          </button>
          <button
            onClick={() => setMode('swipe')}
            className={`px-2.5 py-1 rounded font-medium transition-colors ${
              mode === 'swipe' ? 'bg-white shadow-sm text-blue-700' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Swipe Slider
          </button>
        </div>
      </div>

      {mode === 'side-by-side' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Before Image */}
          <div className="border border-slate-200 rounded-lg overflow-hidden bg-slate-900">
            <div className="bg-slate-800 text-slate-200 px-3 py-1.5 text-xs font-semibold flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-slate-400" />
                Before: {earlierDate}
              </span>
              <span className="text-slate-400">Baseline Pass</span>
            </div>
            <div className="aspect-square relative flex items-center justify-center">
              <img
                src={beforeUrl}
                alt="Baseline satellite observation"
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = 'none';
                }}
              />
              <div className="absolute inset-0 bg-blue-900/10 pointer-events-none" />
            </div>
          </div>

          {/* After Image */}
          <div className="border border-slate-200 rounded-lg overflow-hidden bg-slate-900">
            <div className="bg-blue-900 text-white px-3 py-1.5 text-xs font-semibold flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-blue-300" />
                After: {laterDate}
              </span>
              <span className="text-blue-200">Comparison Pass</span>
            </div>
            <div className="aspect-square relative flex items-center justify-center">
              <img
                src={afterUrl}
                alt="Recent satellite observation"
                className="w-full h-full object-cover"
                onError={(e) => {
                  (e.target as HTMLElement).style.display = 'none';
                }}
              />
              <div className="absolute inset-0 bg-amber-500/10 pointer-events-none" />
            </div>
          </div>
        </div>
      ) : (
        /* Swipe Slider */
        <div className="relative aspect-video max-h-[440px] w-full border border-slate-300 rounded-lg overflow-hidden select-none">
          <img src={afterUrl} alt="After" className="absolute inset-0 w-full h-full object-cover" />
          <div
            className="absolute inset-0 overflow-hidden"
            style={{ width: `${sliderPosition}%` }}
          >
            <img
              src={beforeUrl}
              alt="Before"
              className="absolute inset-0 w-full h-full object-cover max-w-none"
              style={{ width: '100%', height: '100%' }}
            />
          </div>

          {/* Slider Line */}
          <div
            className="absolute top-0 bottom-0 w-1 bg-white shadow-lg cursor-ew-resize flex items-center justify-center"
            style={{ left: `${sliderPosition}%` }}
          >
            <div className="w-6 h-6 bg-white rounded-full shadow border border-slate-300 flex items-center justify-center text-slate-700 text-xs font-bold">
              ↔
            </div>
          </div>

          <input
            type="range"
            min="0"
            max="100"
            value={sliderPosition}
            onChange={(e) => setSliderPosition(Number(e.target.value))}
            className="absolute inset-0 opacity-0 cursor-ew-resize w-full h-full"
          />

          <div className="absolute bottom-3 left-3 bg-black/60 text-white px-2 py-1 rounded text-xs">
            Before: {earlierDate}
          </div>
          <div className="absolute bottom-3 right-3 bg-black/60 text-white px-2 py-1 rounded text-xs">
            After: {laterDate}
          </div>
        </div>
      )}
    </div>
  );
};
