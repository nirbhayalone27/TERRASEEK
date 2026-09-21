import React, { useEffect, useState } from 'react';
import { reviewApi } from '../api/client';
import { ReviewTask } from '../types';
import { CheckSquare, CheckCircle, XCircle, HelpCircle, ArrowRight, ShieldAlert } from 'lucide-react';
import { Link } from 'react-router-dom';

export const ReviewQueue: React.FC = () => {
  const [tasks, setTasks] = useState<ReviewTask[]>([]);
  const [selectedTask, setSelectedTask] = useState<ReviewTask | null>(null);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(true);

  const loadQueue = () => {
    setLoading(true);
    reviewApi
      .getQueue()
      .then((data) => {
        setTasks(data);
        if (data.length > 0 && !selectedTask) {
          setSelectedTask(data[0]);
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadQueue();
  }, []);

  const handleDecision = async (decision: 'APPROVE' | 'REJECT' | 'NEEDS_MORE_EVIDENCE') => {
    if (!selectedTask) return;
    try {
      await reviewApi.submitDecision(selectedTask.id, decision, notes || `Decision ${decision} recorded.`);
      setNotes('');
      loadQueue();
      alert(`Decision recorded: ${decision}`);
    } catch (err: any) {
      alert(err.message || 'Failed to submit decision');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Analyst Review Queue</h1>
          <p className="text-xs text-slate-500">
            Escalated uncertain results and borderline evidence cases awaiting expert ground-truth validation.
          </p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-amber-50 text-amber-800 border border-amber-200 rounded">
          {tasks.length} Pending Task(s)
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Queue List */}
        <div className="lg:col-span-6 space-y-3">
          {loading ? (
            <div className="p-8 text-center text-xs text-slate-500 bg-white rounded border border-slate-200">
              Loading review tasks...
            </div>
          ) : tasks.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-lg border border-slate-200 text-xs text-slate-500">
              No pending review tasks in the queue.
            </div>
          ) : (
            tasks.map((task) => {
              const isSelected = selectedTask?.id === task.id;
              return (
                <div
                  key={task.id}
                  onClick={() => setSelectedTask(task)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    isSelected
                      ? 'bg-blue-50/50 border-blue-500 shadow-sm'
                      : 'bg-white border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <h3 className="text-sm font-bold text-slate-900">{task.site_name || task.site_id}</h3>
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-amber-100 text-amber-800 rounded">
                      {task.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-600 mb-2 font-mono">Query: "{task.query}"</div>
                  <div className="p-2 bg-slate-50 rounded border border-slate-100 text-xs text-slate-700">
                    <span className="font-semibold block text-slate-800">Escalation Reason:</span>
                    {task.reason}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right: Decision Panel */}
        <div className="lg:col-span-6">
          {selectedTask ? (
            <div className="bg-white p-5 rounded-lg border border-slate-200 sticky top-20">
              <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
                <div className="flex items-center gap-1.5 font-bold text-slate-800 text-sm">
                  <ShieldAlert className="w-4 h-4 text-amber-600" />
                  <span>Reviewing Task: {selectedTask.site_name || selectedTask.site_id}</span>
                </div>
                <Link
                  to={`/sites/${selectedTask.site_id}`}
                  className="text-xs text-blue-700 hover:underline flex items-center gap-1 font-medium"
                >
                  <span>Inspect Site</span>
                  <ArrowRight className="w-3 h-3" />
                </Link>
              </div>

              <div className="space-y-3 text-xs text-slate-700 mb-5">
                <div>
                  <span className="text-slate-400 block font-semibold">Flagged Query:</span>
                  <p className="font-mono bg-slate-50 p-2 rounded border border-slate-100">
                    {selectedTask.query}
                  </p>
                </div>

                <div>
                  <span className="text-slate-400 block font-semibold">Flagged By:</span>
                  <p className="font-medium text-slate-800">{selectedTask.flagged_by}</p>
                </div>

                <div>
                  <span className="text-slate-400 block font-semibold">Detailed Reason:</span>
                  <p className="p-2.5 bg-amber-50/60 border border-amber-100 text-amber-900 rounded">
                    {selectedTask.reason}
                  </p>
                </div>

                <div>
                  <label className="block text-slate-700 font-semibold mb-1">
                    Analyst Ground-Truth Determination Notes
                  </label>
                  <textarea
                    rows={3}
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    placeholder="Enter analytical justification..."
                    className="w-full text-xs p-2.5 border border-slate-300 rounded focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => handleDecision('APPROVE')}
                  className="py-2 px-3 bg-green-700 hover:bg-green-800 text-white rounded text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
                >
                  <CheckCircle className="w-3.5 h-3.5" />
                  Approve
                </button>
                <button
                  onClick={() => handleDecision('REJECT')}
                  className="py-2 px-3 bg-rose-700 hover:bg-rose-800 text-white rounded text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
                >
                  <XCircle className="w-3.5 h-3.5" />
                  Reject
                </button>
                <button
                  onClick={() => handleDecision('NEEDS_MORE_EVIDENCE')}
                  className="py-2 px-3 bg-slate-700 hover:bg-slate-800 text-white rounded text-xs font-semibold flex items-center justify-center gap-1 transition-colors"
                >
                  <HelpCircle className="w-3.5 h-3.5" />
                  Need Evidence
                </button>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center bg-white rounded border border-slate-200 text-xs text-slate-400">
              Select a task from the queue to take review action.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
