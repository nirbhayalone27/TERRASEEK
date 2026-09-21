import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { siteApi, evidenceApi, reportsApi } from '../api/client';
import { SiteDetail as SiteDetailType, ObservationRead, ChangeEventRead } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Timeline } from '../components/Timeline';
import { BeforeAfterViewer } from '../components/BeforeAfterViewer';
import {
  MapPin,
  Calendar,
  Compass,
  Clock,
  Activity,
  ArrowLeft,
  FileText,
  CheckSquare,
  ShieldCheck,
  Eye,
} from 'lucide-react';

export const SiteDetail: React.FC = () => {
  const { siteId } = useParams<{ siteId: string }>();
  const navigate = useNavigate();

  const [site, setSite] = useState<SiteDetailType | null>(null);
  const [observations, setObservations] = useState<ObservationRead[]>([]);
  const [changes, setChanges] = useState<ChangeEventRead[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewMessage, setReviewMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!siteId) return;
    setLoading(true);

    Promise.all([
      siteApi.get(siteId),
      siteApi.getObservations(siteId),
      siteApi.getChanges(siteId),
    ])
      .then(([s, obs, chgs]) => {
        setSite(s);
        setObservations(obs);
        setChanges(chgs);
      })
      .catch((err) => setError(err.message || 'Failed to load site details'))
      .finally(() => setLoading(false));
  }, [siteId]);

  const handleGenerateReport = async () => {
    if (!site) return;
    try {
      const rep = await reportsApi.generate(site.id, 'Site Investigation Analysis');
      navigate(`/reports/${rep.id}`);
    } catch (err: any) {
      alert(err.message || 'Failed to generate report');
    }
  };

  const handleSendToReview = async () => {
    if (!site) return;
    try {
      await evidenceApi.escalateToReview(
        site.latest_evidence_id || site.id,
        'Analyst manual inspection requested from site detail page.'
      );
      setReviewMessage('Site successfully submitted to analyst review queue.');
      setTimeout(() => setReviewMessage(null), 4000);
    } catch (err: any) {
      alert(err.message || 'Failed to escalate to review');
    }
  };

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12 text-center text-sm text-slate-500">
        Loading satellite site data and observations...
      </div>
    );
  }

  if (error || !site) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-12 text-center">
        <p className="text-sm text-rose-600 mb-4">{error || 'Site not found'}</p>
        <Link to="/search" className="text-xs font-semibold text-blue-700 hover:underline">
          ← Return to Search
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      {/* Back Navigation */}
      <Link
        to="/search"
        className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 mb-4 transition-colors"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        Back to Search Results
      </Link>

      {/* Review Confirmation Message */}
      {reviewMessage && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md text-green-800 text-xs flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-green-600" />
          <span>{reviewMessage}</span>
        </div>
      )}

      {/* Site Header Card */}
      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h1 className="text-xl font-bold text-slate-900">{site.name}</h1>
              <StatusBadge status={site.evidence_status} size="md" />
            </div>
            <div className="flex items-center gap-1.5 text-xs text-slate-500">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{site.location_name}</span>
              <span className="text-slate-300">|</span>
              <span>
                Coordinates: {site.latitude.toFixed(4)}°N, {site.longitude.toFixed(4)}°E
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2 flex-wrap">
            <button
              onClick={handleGenerateReport}
              className="px-3 py-2 bg-blue-700 hover:bg-blue-800 text-white rounded-md text-xs font-medium transition-colors flex items-center gap-1.5 shadow-sm"
            >
              <FileText className="w-3.5 h-3.5" />
              Generate Report
            </button>
            <button
              onClick={handleSendToReview}
              className="px-3 py-2 bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 rounded-md text-xs font-medium transition-colors flex items-center gap-1.5"
            >
              <CheckSquare className="w-3.5 h-3.5" />
              Send to Review
            </button>
            {site.latest_evidence_id && (
              <Link
                to={`/evidence/${site.latest_evidence_id}`}
                className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-md text-xs font-medium transition-colors flex items-center gap-1.5"
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                View Evidence
              </Link>
            )}
          </div>
        </div>

        {/* Verification Summary Matrix */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
          <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 mb-1">
              <Compass className="w-4 h-4 text-blue-700" />
              <span>Spatial Verification</span>
            </div>
            <p className="text-xs text-slate-600">
              {site.spatial_verification_summary || 'Verified within distance bounds.'}
            </p>
          </div>

          <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 mb-1">
              <Clock className="w-4 h-4 text-blue-700" />
              <span>Temporal Verification</span>
            </div>
            <p className="text-xs text-slate-600">
              {site.temporal_verification_summary || 'Multi-pass observations available.'}
            </p>
          </div>

          <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 mb-1">
              <Activity className="w-4 h-4 text-blue-700" />
              <span>Change Evidence</span>
            </div>
            <p className="text-xs text-slate-600">
              {site.change_evidence_summary || 'Surface delta detected.'}
            </p>
          </div>
        </div>
      </div>

      {/* Before / After Viewer */}
      <div className="mb-6">
        <BeforeAfterViewer
          siteId={site.id}
          earlierDate={site.earliest_observation_date || undefined}
          laterDate={site.latest_observation_date || undefined}
        />
      </div>

      {/* Observation Timeline */}
      <div className="mb-6">
        <Timeline
          observations={observations}
          earliestSupportedDate={site.earliest_observation_date}
        />
      </div>
    </div>
  );
};
