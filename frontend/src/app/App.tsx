import { useCallback, useEffect, useState } from 'react'

import { ErrorBanner } from '../components/ErrorBanner'
import { ActivityIcon } from '../components/Icons'
import { AnalysisList } from '../features/analyses/AnalysisList'
import { AnalysisSetup } from '../features/analyses/AnalysisSetup'
import { VideoUpload } from '../features/videos/VideoUpload'
import { ApiError, api } from '../lib/api'
import type { Analysis, CreateAnalysisInput, Video } from '../types/domain'

function readableError(error: unknown): string {
  if (error instanceof ApiError || error instanceof Error) return error.message
  return 'Something went wrong. Please try again.'
}

export function App() {
  const [videos, setVideos] = useState<Video[]>([])
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [selectedVideoId, setSelectedVideoId] = useState('')
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [cancellingId, setCancellingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const refreshAnalyses = useCallback(async () => {
    try {
      const page = await api.listAnalyses()
      setAnalyses(page.items)
    } catch {
      // Keep existing data during background polling; explicit actions surface errors.
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    Promise.all([api.listVideos(), api.listAnalyses()])
      .then(([videoPage, analysisPage]) => {
        if (cancelled) return
        setVideos(videoPage.items)
        setAnalyses(analysisPage.items)
        setError(null)
      })
      .catch((cause: unknown) => {
        if (!cancelled) setError(readableError(cause))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    const active = analyses.some(({ status }) =>
      ['queued', 'running'].includes(status),
    )
    if (!active) return undefined
    const timer = window.setInterval(() => void refreshAnalyses(), 5000)
    return () => window.clearInterval(timer)
  }, [analyses, refreshAnalyses])

  async function uploadVideo(file: File): Promise<Video> {
    setUploading(true)
    setError(null)
    try {
      const uploaded = await api.uploadVideo(file)
      setVideos((current) => [uploaded, ...current])
      setSelectedVideoId(uploaded.id)
      return uploaded
    } catch (cause) {
      setError(readableError(cause))
      throw cause
    } finally {
      setUploading(false)
    }
  }

  async function createAnalysis(input: CreateAnalysisInput): Promise<Analysis> {
    setCreating(true)
    setError(null)
    try {
      const analysis = await api.createAnalysis(input)
      setAnalyses((current) => [analysis, ...current])
      return analysis
    } catch (cause) {
      setError(readableError(cause))
      throw cause
    } finally {
      setCreating(false)
    }
  }

  async function cancelAnalysis(id: string): Promise<void> {
    setCancellingId(id)
    setError(null)
    try {
      const cancelled = await api.cancelAnalysis(id)
      setAnalyses((current) =>
        current.map((item) => (item.id === id ? cancelled : item)),
      )
    } catch (cause) {
      setError(readableError(cause))
    } finally {
      setCancellingId(null)
    }
  }

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="Corner Vision home">
          <span className="brand-mark">CV</span>
          <span>
            <strong>Corner Vision</strong>
            <small>Boxing intelligence</small>
          </span>
        </a>
        <div className="system-state">
          <span className="state-dot" />
          API workspace
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-copy">
            <span className="kicker"><ActivityIcon size={17} /> Fight analysis lab</span>
            <h1>See the round.<br /><em>Read the fight.</em></h1>
            <p>
              Turn boxing footage into structured, reviewable punch events with
              a confidence-aware computer vision workflow.
            </p>
          </div>
          <div className="hero-stat" aria-label="Current workspace statistics">
            <span>Workspace</span>
            <strong>{videos.length.toString().padStart(2, '0')}</strong>
            <small>uploaded rounds</small>
          </div>
        </section>

        {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

        {loading ? (
          <div className="loading-state" role="status">
            <span className="spinner" /> Loading workspace…
          </div>
        ) : (
          <>
            <div className="workflow-grid">
              <VideoUpload uploading={uploading} onUpload={uploadVideo} />
              <AnalysisSetup
                videos={videos}
                selectedVideoId={selectedVideoId}
                creating={creating}
                onSelectedVideoChange={setSelectedVideoId}
                onCreate={createAnalysis}
              />
            </div>
            <AnalysisList
              analyses={analyses}
              videos={videos}
              cancellingId={cancellingId}
              onCancel={cancelAnalysis}
            />
          </>
        )}
      </main>

      <footer>
        <span>Corner Vision · Research prototype</span>
        <span>Outcomes are analytical estimates, not official judging.</span>
      </footer>
    </div>
  )
}
