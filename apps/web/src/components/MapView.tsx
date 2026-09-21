import React, { useEffect, useRef, useState } from 'react';
import { SearchResultItem } from '../types';
import { MapControls } from './MapControls';
import { MapPin, Navigation, Crosshair } from 'lucide-react';

interface Props {
  results: SearchResultItem[];
  selectedResult?: SearchResultItem | null;
  onSelectSite?: (site: SearchResultItem) => void;
  center?: [number, number];
  zoom?: number;
}

export const MapView: React.FC<Props> = ({
  results,
  selectedResult,
  onSelectSite,
  center = [12.0, 49.0],
  zoom = 5,
}) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const [currentCenter, setCurrentCenter] = useState<[number, number]>(center);
  const [currentZoom, setCurrentZoom] = useState<number>(zoom);

  useEffect(() => {
    if (selectedResult) {
      setCurrentCenter([selectedResult.longitude, selectedResult.latitude]);
      setCurrentZoom(8);
    }
  }, [selectedResult]);

  const handleZoomIn = () => setCurrentZoom((z) => Math.min(z + 1, 14));
  const handleZoomOut = () => setCurrentZoom((z) => Math.max(z - 1, 2));
  const handleReset = () => {
    setCurrentCenter(center);
    setCurrentZoom(zoom);
  };

  return (
    <div className="relative w-full h-full min-h-[420px] bg-slate-100 rounded-lg border border-slate-200 overflow-hidden flex flex-col">
      {/* Top Map Header */}
      <div className="absolute top-3 left-3 z-10 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-md border border-slate-200 shadow-sm flex items-center gap-2 text-xs">
        <Navigation className="w-3.5 h-3.5 text-blue-700" />
        <span className="font-semibold text-slate-800">Satellite Map View</span>
        <span className="text-slate-400">|</span>
        <span className="text-slate-500">
          Lon: {currentCenter[0].toFixed(2)}°, Lat: {currentCenter[1].toFixed(2)}° (Zoom: {currentZoom})
        </span>
      </div>

      <MapControls onZoomIn={handleZoomIn} onZoomOut={handleZoomOut} onReset={handleReset} />

      {/* Offline Geo-Canvas & Interactive Map Surface */}
      <div className="relative flex-1 bg-slate-900 overflow-hidden select-none">
        {/* Synthetic Satellite Grid Pattern & Elevation Relief */}
        <svg className="absolute inset-0 w-full h-full opacity-60">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpace">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#334155" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* River Representation for Central Europe Basin */}
          <path
            d="M 50 180 Q 200 220 380 190 T 700 310"
            fill="none"
            stroke="#2563eb"
            strokeWidth="4"
            opacity="0.7"
          />
          {/* Major Road Arterial */}
          <path
            d="M 120 60 L 320 210 L 520 280"
            fill="none"
            stroke="#94a3b8"
            strokeWidth="2"
            strokeDasharray="4 2"
            opacity="0.6"
          />
        </svg>

        {/* Dynamic Markers for Results */}
        <div className="absolute inset-0 p-8 flex items-center justify-center">
          <div className="relative w-full h-full max-w-2xl max-h-[360px]">
            {results.map((r, idx) => {
              const isSelected = selectedResult?.site_id === r.site_id;
              // Project relative offsets for demo layout
              const leftOffsets = ['28%', '65%', '48%', '34%', '58%'];
              const topOffsets = ['42%', '30%', '55%', '68%', '75%'];
              const left = leftOffsets[idx % leftOffsets.length];
              const top = topOffsets[idx % topOffsets.length];

              return (
                <div
                  key={r.site_id}
                  style={{ left, top }}
                  onClick={() => onSelectSite?.(r)}
                  className={`absolute -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-transform ${
                    isSelected ? 'scale-110 z-20' : 'hover:scale-105 z-10'
                  }`}
                >
                  <div
                    className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold shadow-md border ${
                      isSelected
                        ? 'bg-blue-600 text-white border-blue-400 ring-4 ring-blue-500/30'
                        : 'bg-white text-slate-900 border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    <MapPin className={`w-3.5 h-3.5 ${isSelected ? 'text-white' : 'text-blue-600'}`} />
                    <span>{r.site_name.split(' - ')[0]}</span>
                    {r.status === 'SUPPORTED' && (
                      <span className="w-2 h-2 rounded-full bg-green-500" />
                    )}
                  </div>

                  {/* Footprint Box if Selected */}
                  {isSelected && (
                    <div className="absolute -inset-4 border-2 border-dashed border-blue-400 bg-blue-500/10 rounded pointer-events-none animate-pulse" />
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Bottom Legend */}
        <div className="absolute bottom-3 left-3 bg-slate-900/80 backdrop-blur-sm px-3 py-2 rounded border border-slate-700 text-xs text-slate-300 flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-green-500"></span>
            <span>Supported</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
            <span>Needs Review</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-blue-500"></span>
            <span>River Channel</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-0.5 bg-slate-400 border-dashed"></span>
            <span>Roadway</span>
          </div>
        </div>
      </div>
    </div>
  );
};
