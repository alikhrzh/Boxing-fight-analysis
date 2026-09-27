import type {
  Analysis,
  CreateAnalysisInput,
  Page,
  Video,
} from '../types/domain'

const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? '/api/v1').replace(/\/$/, '')

interface ApiErrorBody {
  error?: {
    code?: string
    message?: string
  }
}

export class ApiError extends Error {
  readonly status: number
  readonly code: string

  constructor(message: string, status: number, code = 'request_failed') {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...init?.headers,
    },
  })

  if (!response.ok) {
    let body: ApiErrorBody | undefined
    try {
      body = (await response.json()) as ApiErrorBody
    } catch {
      body = undefined
    }
    throw new ApiError(
      body?.error?.message ?? `Request failed with status ${response.status}.`,
      response.status,
      body?.error?.code,
    )
  }

  if (response.status === 204) {
    return undefined as T
  }
  return (await response.json()) as T
}

export const api = {
  listVideos: () => request<Page<Video>>('/videos?limit=100'),

  uploadVideo: (file: File) => {
    const form = new FormData()
    form.append('file', file)
    return request<Video>('/videos', { method: 'POST', body: form })
  },

  deleteVideo: (videoId: string) =>
    request<void>(`/videos/${videoId}`, { method: 'DELETE' }),

  listAnalyses: () => request<Page<Analysis>>('/analyses?limit=100'),

  createAnalysis: (input: CreateAnalysisInput) =>
    request<Analysis>('/analyses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input),
    }),

  cancelAnalysis: (analysisId: string) =>
    request<Analysis>(`/analyses/${analysisId}/cancel`, { method: 'POST' }),
}
