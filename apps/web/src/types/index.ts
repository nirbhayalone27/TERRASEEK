export type EvidenceStatus = 'SUPPORTED' | 'NEEDS_REVIEW' | 'INSUFFICIENT_EVIDENCE' | 'NO_MATCH';

export type ChangeType = 'BUILDING' | 'ROAD' | 'VEGETATION' | 'WATER' | 'UNKNOWN';

export type JobStatus = 'QUEUED' | 'RUNNING' | 'SUCCEEDED' | 'FAILED' | 'CANCELLED';

export interface SearchResultItem {
  site_id: string;
  site_name: string;
  location_name: string;
  change_type: ChangeType;
  earlier_date?: string;
  later_date?: string;
  status: EvidenceStatus;
  evidence_summary: string;
  spatial_summary: string;
  temporal_summary: string;
  change_summary: string;
  latitude: number;
  longitude: number;
  geometry?: any;
  relevance_score?: number;
  evidence_id?: string;
}

export interface SimilarRetrievalItem {
  site_id: string;
  site_name: string;
  location_name: string;
  similarity_score: number;
  acquisition_date?: string;
  thumbnail_url?: string;
  latitude: number;
  longitude: number;
  evidence_status: EvidenceStatus;
  model_provider?: string;
}

export interface MissionIntent {
  raw_query: string;
  target_entity: string;
  change_detected_required: boolean;
  change_type: ChangeType;
  spatial_constraints: Array<{
    feature: string;
    distance_meters: number;
    relation: string;
  }>;
  temporal_required: boolean;
  earlier_imagery_required: boolean;
  is_known_unmatchable: boolean;
}

export interface SearchResponse {
  query: string;
  mission: MissionIntent;
  status: EvidenceStatus;
  total_results: number;
  results: SearchResultItem[];
  execution_plan: string[];
  summary: string;
}

export interface SiteDetail {
  id: string;
  name: string;
  location_name: string;
  latitude: number;
  longitude: number;
  boundary?: any;
  description?: string;
  tags: string[];
  metadata: Record<string, any>;
  created_at: string;
  primary_change_type?: ChangeType;
  evidence_status: EvidenceStatus;
  earliest_observation_date?: string;
  latest_observation_date?: string;
  spatial_verification_summary?: string;
  temporal_verification_summary?: string;
  change_evidence_summary?: string;
  latest_evidence_id?: string;
}

export interface ObservationRead {
  id: string;
  site_id: string;
  acquisition_date: string;
  sensor: string;
  resolution_meters: number;
  cloud_cover: number;
  usable: boolean;
  asset_path?: string;
  thumbnail_url?: string;
  bands: string[];
  metadata: Record<string, any>;
  created_at: string;
}

export interface ChangeEventRead {
  id: string;
  site_id: string;
  change_type: ChangeType;
  earlier_date: string;
  later_date: string;
  earlier_observation_id?: string;
  later_observation_id?: string;
  area_sq_meters: number;
  status: string;
  model_name: string;
  model_tier: string;
  geometry?: any;
  created_at: string;
}

export interface EvidenceItem {
  id: string;
  evidence_type: string;
  title: string;
  description: string;
  status: EvidenceStatus;
  source: string;
  asset_id?: string;
  observation_id?: string;
  method: string;
  timestamp: string;
  geometry?: any;
  metadata?: Record<string, any>;
}

export interface EvidencePassport {
  id: string;
  site_id: string;
  query: string;
  status: EvidenceStatus;
  items: EvidenceItem[];
  spatial_summary: string;
  temporal_summary: string;
  change_summary: string;
  model_provenance: Record<string, any>;
  limitations: string[];
  created_at: string;
  needs_review_reason?: string;
}

export interface ReviewTask {
  id: string;
  site_id: string;
  site_name?: string;
  evidence_id: string;
  query: string;
  reason: string;
  flagged_by: string;
  status: string;
  created_at: string;
}

export interface JobRead {
  id: string;
  job_type: string;
  status: JobStatus;
  progress_percentage: number;
  created_at: string;
  started_at?: string;
  finished_at?: string;
  error_message?: string;
  payload: Record<string, any>;
  result?: Record<string, any>;
}

export interface ReportRead {
  id: string;
  site_id: string;
  site_name: string;
  query: string;
  status: EvidenceStatus;
  observation_timeline: Array<Record<string, any>>;
  spatial_verification: Record<string, any>;
  change_analysis: Record<string, any>;
  temporal_verification: Record<string, any>;
  evidence_items: EvidenceItem[];
  model_provenance: Record<string, any>;
  limitations: string[];
  conclusion: string;
  created_at: string;
  format: string;
}
