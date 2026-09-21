import React from 'react';
import { ObservationRead } from '../types';
import { Calendar, CheckCircle2, Clock, Eye } from 'lucide-react';

interface Props {
  observations: ObservationRead[];
  earliestSupportedDate?: string | null;
}

export const Timeline: React.FC<Props> = ({ observations, earliestSupportedDate }) => {
  const sorted = [...observations].sort(
    (a, b) => new Date(a.acquisition_date).getTime() - new Date(b.acquisition_date).getTime()
  );

  return (
    <div className="bg-white p-5 rounded-lg border border-slate-200">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-blue-700" />
          <h4 className="text-sm font-bold text-slate-900">Observation Timeline & Temporal Continuity</h4>
        </div>
        <span className="text-xs text-slate-500 font-medium">
          {sorted.length} satellite observation(s)
        </span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-200">
        {sorted.map((obs, idx) => {
          const obsDate = new Date(obs.acquisition_date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          });
          const isEarliest = earliestSupportedDate && obsDate.includes(earliestSupportedDate);
          const isFirst = idx === 0;
          const isLatest = idx === sorted.length - 1;

          return (
            <div key={obs.id} className="relative">
              {/* Timeline marker */}
              <div
                className={`absolute -left-6 top-1 w-3.5 h-3.5 rounded-full border-2 bg-white flex items-center justify-center ${
                  isEarliest || isFirst || isLatest
                    ? 'border-blue-600 ring-2 ring-blue-100'
                    : 'border-slate-400'
                }`}
              />

              <div className="bg-slate-50 p-3 rounded-md border border-slate-200">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-1.5 font-semibold text-xs text-slate-800">
                    <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    <span>{obsDate}</span>
                  </div>
                  {isEarliest ? (
                    <span className="text-xs font-semibold px-2 py-0.5 bg-blue-100 text-blue-800 rounded border border-blue-200 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      Earliest Supported Observation
                    </span>
                  ) : isFirst ? (
                    <span className="text-xs text-slate-500 bg-slate-200 px-1.5 py-0.5 rounded">Baseline</span>
                  ) : isLatest ? (
                    <span className="text-xs text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded">Latest Pass</span>
                  ) : null}
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs text-slate-600 mt-2">
                  <div>
                    <span className="text-slate-400 block">Sensor:</span>
                    <span className="font-medium text-slate-700">{obs.sensor}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Resolution:</span>
                    <span className="font-medium text-slate-700">{obs.resolution_meters}m GSD</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Cloud Cover:</span>
                    <span className="font-medium text-slate-700">{obs.cloud_cover}%</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Usable:</span>
                    <span className="font-medium text-green-700">Verified Usable</span>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
