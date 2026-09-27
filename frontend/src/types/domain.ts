export interface Pagination {
  limit: number
  offset: number
  total: number
}

export interface Page<T> {
  items: T[]
  pagination: Pagination
}

export interface Video {
  id: string
  original_name: string
  content_type: string | null
  size_bytes: number
  sha256: string
  created_at: string
}

export type AnalysisStatus =
  | 'queued'
  | 'running'
  | 'completed'
  | 'failed'
  | 'cancelled'

export interface AnalysisResult {
  [key: string]: unknown
}

export interface Analysis {
  id: string
  video_id: string
  round_number: number
  status: AnalysisStatus
  progress: number
  current_stage: string
  config: Record<string, unknown>
  result: AnalysisResult | null
  error_code: string | null
  error_message: string | null
  created_at: string
  updated_at: string
  started_at: string | null
  completed_at: string | null
}

export interface CreateAnalysisInput {
  video_id: string
  round_number: number
  config: {
    pose_model: string
  }
}
