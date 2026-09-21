import React, { useState } from 'react';
import { retrievalApi } from '../api/client';
import { SimilarRetrievalItem } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Upload, Layers, MapPin, Calendar, ArrowRight, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';

export const FindSimilar: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [results, setResults] = useState<SimilarRetrievalItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [providerInfo, setProviderInfo] = useState<string>('DemoEmbeddingProvider');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    const formData = new FormData();
    if (selectedFile) {
      formData.append('image', selectedFile);
    }
    formData.append('limit', '5');

    try {
      const data = await retrievalApi.findSimilar(formData);
      setResults(data.results || []);
      setProviderInfo(data.model_provider || 'DemoEmbeddingProvider');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Find Similar Satellite Places</h1>
        <p className="text-xs text-slate-500">
          Upload an optical image patch or raster to retrieve matching locations based on visual and semantic features.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Upload Container */}
        <div className="bg-white p-5 rounded-lg border border-slate-200">
          <label className="block text-xs font-semibold text-slate-700 mb-2">
            Upload Reference Satellite Image
          </label>
          <div className="border-2 border-dashed border-slate-300 hover:border-blue-500 rounded-lg p-6 text-center cursor-pointer transition-colors bg-slate-50">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              {previewUrl ? (
                <img src={previewUrl} alt="Preview" className="max-h-40 mx-auto rounded mb-2 object-cover" />
              ) : (
                <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
              )}
              <span className="text-xs text-blue-700 font-medium block">
                {selectedFile ? selectedFile.name : 'Select or drop an image file'}
              </span>
              <span className="text-[10px] text-slate-400 block mt-1">PNG, JPEG, GeoTIFF thumbnail</span>
            </label>
          </div>

          <button
            onClick={handleSearch}
            disabled={loading}
            className="w-full mt-4 py-2 px-4 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white text-xs font-medium rounded-md transition-colors flex items-center justify-center gap-1.5 shadow-sm"
          >
            <Layers className="w-4 h-4" />
            {loading ? 'Generating Vector Embeddings...' : 'Find Similar Locations'}
          </button>

          <div className="mt-4 p-2.5 bg-slate-100 rounded text-[11px] text-slate-600">
            <span className="font-semibold block text-slate-700">Model Provider:</span>
            <span className="font-mono text-slate-800">{providerInfo}</span>
            <span className="block text-slate-500 mt-0.5">
              (Deterministic local vector projection mode active)
            </span>
          </div>
        </div>

        {/* Results Column */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Retrieved Similar Candidates ({results.length})
            </span>
            <span className="text-xs text-slate-500">Ranked by Cosine Similarity</span>
          </div>

          {results.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-lg border border-slate-200 text-xs text-slate-500">
              Upload an image patch above or click "Find Similar Locations" to run retrieval across catalog embeddings.
            </div>
          ) : (
            results.map((item) => (
              <div
                key={item.site_id}
                className="p-4 bg-white rounded-lg border border-slate-200 hover:border-slate-300 flex items-start justify-between gap-4 transition-all shadow-sm"
              >
                <div className="flex items-start gap-3">
                  <div className="w-16 h-16 rounded bg-slate-800 shrink-0 overflow-hidden border border-slate-200">
                    <img
                      src={item.thumbnail_url}
                      alt="Thumbnail"
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        (e.target as HTMLElement).style.display = 'none';
                      }}
                    />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="text-sm font-bold text-slate-900">{item.site_name}</h4>
                      <StatusBadge status={item.evidence_status} size="sm" />
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-500 mb-1">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                        {item.location_name}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-slate-400" />
                        {item.acquisition_date}
                      </span>
                    </div>
                    <div className="text-xs font-medium text-slate-700">
                      Similarity: <span className="font-mono text-blue-700">{item.similarity_score}</span>
                    </div>
                  </div>
                </div>

                <Link
                  to={`/sites/${item.site_id}`}
                  className="shrink-0 p-2 text-blue-700 hover:bg-blue-50 rounded transition-colors text-xs font-semibold flex items-center gap-1"
                >
                  <span>View</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
