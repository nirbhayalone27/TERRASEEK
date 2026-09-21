import {
  SearchResponse,
  SiteDetail,
  ObservationRead,
  ChangeEventRead,
  EvidencePassport,
  ReviewTask,
  JobRead,
  ReportRead,
} from '../types';

const API_BASE = '/api/v1';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson?.error?.message || errJson?.detail || response.statusText;
    } catch {
      errorDetail = response.statusText;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export const searchApi = {
  search: (query: string, limit: number = 10) =>
    request<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    }),
};

export const siteApi = {
  list: (limit: number = 20) => request<SiteDetail[]>(`/sites?limit=${limit}`),
  get: (siteId: string) => request<SiteDetail>(`/sites/${siteId}`),
  getObservations: (siteId: string) => request<ObservationRead[]>(`/sites/${siteId}/observations`),
  getChanges: (siteId: string) => request<ChangeEventRead[]>(`/sites/${siteId}/changes`),
};

export const retrievalApi = {
  findSimilar: async (formData: FormData) => {
    const res = await fetch(`${API_BASE}/retrieval/similar`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to retrieve similar observations');
    return res.json();
  },
};

export const changeApi = {
  analyze: (siteId: string, earlierDate?: string, laterDate?: string, changeTypes?: string[]) =>
    request('/change/analyze', {
      method: 'POST',
      body: JSON.stringify({
        site_id: siteId,
        earlier_date: earlierDate,
        later_date: laterDate,
        change_types: changeTypes || ['BUILDING'],
      }),
    }),
  compare: async (formData: FormData) => {
    const res = await fetch(`${API_BASE}/change/compare`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Failed to run change comparison');
    return res.json();
  },
};

export const evidenceApi = {
  get: (evidenceId: string) => request<EvidencePassport>(`/evidence/${evidenceId}`),
  escalateToReview: (evidenceId: string, reason: string) =>
    request(`/evidence/${evidenceId}/review?reason=${encodeURIComponent(reason)}`, {
      method: 'POST',
    }),
};

export const reviewApi = {
  getQueue: (status: string = 'PENDING') => request<ReviewTask[]>(`/review/queue?status=${status}`),
  submitDecision: (taskId: string, decision: 'APPROVE' | 'REJECT' | 'NEEDS_MORE_EVIDENCE', notes: string) =>
    request(`/review/${taskId}/decision`, {
      method: 'POST',
      body: JSON.stringify({
        decision,
        reviewer_notes: notes,
        reviewer_id: 'analyst_1',
      }),
    }),
};

export const jobsApi = {
  submit: (jobType: string, payload: Record<string, any>) =>
    request<JobRead>('/jobs', {
      method: 'POST',
      body: JSON.stringify({ job_type: jobType, payload }),
    }),
  get: (jobId: string) => request<JobRead>(`/jobs/${jobId}`),
};

export const reportsApi = {
  generate: (siteId: string, query: string) =>
    request<ReportRead>('/reports', {
      method: 'POST',
      body: JSON.stringify({ site_id: siteId, query }),
    }),
  get: (reportId: string) => request<ReportRead>(`/reports/${reportId}`),
};
