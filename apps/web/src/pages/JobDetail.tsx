import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { jobsApi } from '../api/client';
import { JobRead } from '../types';
import { Clock, CheckCircle2, AlertCircle, RefreshCw, ArrowLeft } from 'lucide-react';

export const JobDetail: React.FC = () => {
  const { jobId } = useParams<{ jobId: string }>();
  const [job, setJob] = useState<JobRead | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJob = () => {
    if (!jobId) return;
    jobsApi
      .get(jobId)
      .then((data) => setJob(data))
      .catch((err) => setError(err.message || 'Failed to fetch job'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchJob();
    const timer = setInterval(fetchJob, 3000);
    return () => clearInterval(timer);
  }, [jobId]);

  if (loading) {
    return <div className="max-w-3xl mx-auto px-4 py-12 text-center text-xs text-slate-500">Checking job status...</div>;
  }

  if (error || !job) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 text-center">
        <p className="text-sm text-rose-600 mb-3">{error || 'Job not found'}</p>
        <Link to="/search" className="text-xs font-semibold text-blue-700">← Back to Search</Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
      <Link to="/search" className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 mb-4">
        <ArrowLeft className="w-3.5 h-3.5" />
        Back to Search
      </Link>

      <div className="bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
          <div>
            <span className="text-xs font-mono text-slate-400 block">JOB #{job.id}</span>
            <h1 className="text-lg font-bold text-slate-900 capitalize">{job.job_type} Task</h1>
          </div>
          <span className="px-2.5 py-1 rounded text-xs font-bold bg-blue-50 text-blue-700 border border-blue-200">
            {job.status}
          </span>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-xs text-slate-600 mb-1">
            <span>Progress</span>
            <span className="font-mono">{job.progress_percentage}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div
              className="bg-blue-600 h-2 transition-all duration-300"
              style={{ width: `${job.progress_percentage}%` }}
            />
          </div>
        </div>

        {/* Metadata Details */}
        <div className="grid grid-cols-2 gap-4 text-xs bg-slate-50 p-4 rounded border border-slate-200 mb-4">
          <div>
            <span className="text-slate-400 block font-semibold">Created At</span>
            <span>{new Date(job.created_at).toLocaleTimeString()}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-semibold">Finished At</span>
            <span>{job.finished_at ? new Date(job.finished_at).toLocaleTimeString() : 'In Progress...'}</span>
          </div>
        </div>

        {job.result && (
          <div className="text-xs bg-slate-50 p-3 rounded border border-slate-200">
            <span className="font-semibold block text-slate-700 mb-1">Job Result Output:</span>
            <pre className="font-mono text-slate-800">{JSON.stringify(job.result, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};
