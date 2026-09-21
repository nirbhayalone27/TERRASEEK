import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { evidenceApi } from '../api/client';
import { EvidencePassport } from '../types';
import { EvidencePanel } from '../components/EvidencePanel';
import { ArrowLeft, ShieldCheck, CheckSquare } from 'lucide-react';

export const EvidenceDetail: React.FC = () => {
  const { evidenceId } = useParams<{ evidenceId: string }>();
  const [passport, setPassport] = useState<EvidencePassport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [escalated, setEscalated] = useState(false);

  useEffect(() => {
    if (!evidenceId) return;
    setLoading(true);
    evidenceApi
      .get(evidenceId)
      .then((data) => setPassport(data))
      .catch((err) => setError(err.message || 'Failed to load evidence passport'))
      .finally(() => setLoading(false));
  }, [evidenceId]);

  const handleEscalate = async () => {
    if (!evidenceId) return;
    try {
      await evidenceApi.escalateToReview(evidenceId, 'Escalated from evidence passport inspection page.');
      setEscalated(true);
    } catch (err: any) {
      alert(err.message || 'Failed to escalate');
    }
  };

  if (loading) {
    return <div className="max-w-4xl mx-auto px-4 py-12 text-center text-xs text-slate-500">Loading evidence passport...</div>;
  }

  if (error || !passport) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <p className="text-sm text-rose-600 mb-3">{error || 'Evidence not found'}</p>
        <Link to="/search" className="text-xs font-semibold text-blue-700">← Back to Search</Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <div className="flex items-center justify-between mb-4">
        <Link
          to={`/sites/${passport.site_id}`}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Site Investigation
        </Link>

        <button
          onClick={handleEscalate}
          disabled={escalated}
          className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white rounded text-xs font-medium flex items-center gap-1.5"
        >
          <CheckSquare className="w-3.5 h-3.5" />
          {escalated ? 'Escalated to Review' : 'Send to Human Review'}
        </button>
      </div>

      <EvidencePanel passport={passport} onSendToReview={handleEscalate} />
    </div>
  );
};
