import React, { useState } from 'react';
import { Search, CornerDownLeft } from 'lucide-react';

interface Props {
  initialQuery?: string;
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

export const SearchBox: React.FC<Props> = ({ initialQuery = '', onSearch, isLoading = false }) => {
  const [query, setQuery] = useState(initialQuery);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const sampleQueries = [
    'New buildings near a river',
    'Road development',
    'Vegetation loss',
    'Water change',
    'New airport',
    'New construction where earlier imagery is unavailable',
  ];

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <Search className="w-5 h-5" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="What are you looking for? (e.g. New buildings near a river)"
          className="w-full pl-10 pr-24 py-3 bg-white text-slate-900 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent shadow-sm"
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="absolute right-1.5 px-4 py-2 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white font-medium rounded-md text-xs transition-colors flex items-center gap-1.5 shadow-sm"
        >
          {isLoading ? (
            <span>Searching...</span>
          ) : (
            <>
              <span>Search</span>
              <CornerDownLeft className="w-3.5 h-3.5" />
            </>
          )}
        </button>
      </form>

      <div className="mt-2.5 flex items-center gap-1.5 flex-wrap text-xs text-slate-500">
        <span className="font-medium text-slate-600">Examples:</span>
        {sampleQueries.map((sq) => (
          <button
            key={sq}
            type="button"
            onClick={() => {
              setQuery(sq);
              onSearch(sq);
            }}
            className="px-2 py-0.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded border border-slate-200 transition-colors"
          >
            {sq}
          </button>
        ))}
      </div>
    </div>
  );
};
