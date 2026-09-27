import { ActivityIcon } from '../../components/Icons'
import { formatDate, shortId } from '../../lib/format'
import type { Analysis, Video } from '../../types/domain'

interface AnalysisListProps {
  analyses: Analysis[]
  videos: Video[]
  cancellingId: string | null
  onCancel: (id: string) => Promise<void>
}

const statusLabels = {
  queued: 'Queued',
  running: 'Processing',
  completed: 'Complete',
  failed: 'Failed',
  cancelled: 'Cancelled',
} as const

export function AnalysisList({
  analyses,
  videos,
  cancellingId,
  onCancel,
}: AnalysisListProps) {
  const videoNames = new Map(videos.map((video) => [video.id, video.original_name]))

  return (
    <section className="jobs-section" aria-labelledby="jobs-heading">
      <div className="section-title-row">
        <div>
          <span className="eyebrow">Workspace</span>
          <h2 id="jobs-heading">Analysis jobs</h2>
        </div>
        <span className="job-count">{analyses.length} total</span>
      </div>

      {analyses.length === 0 ? (
        <div className="empty-jobs">
          <ActivityIcon size={28} />
          <h3>No analysis jobs yet</h3>
          <p>Your queued and completed rounds will appear here.</p>
        </div>
      ) : (
        <div className="jobs-grid">
          {analyses.map((analysis) => {
            const canCancel = ['queued', 'running'].includes(analysis.status)
            return (
              <article className="job-card" key={analysis.id}>
                <div className="job-topline">
                  <span className={`status status-${analysis.status}`}>
                    <i />{statusLabels[analysis.status]}
                  </span>
                  <span className="job-id">#{shortId(analysis.id)}</span>
                </div>
                <h3>{videoNames.get(analysis.video_id) ?? 'Deleted video'}</h3>
                <div className="job-meta">
                  <span>Round {analysis.round_number}</span>
                  <span>{formatDate(analysis.created_at)}</span>
                </div>

                <div className="progress-block">
                  <div className="progress-copy">
                    <span>{analysis.current_stage}</span>
                    <strong>{Math.round(analysis.progress * 100)}%</strong>
                  </div>
                  <div
                    className="progress-track"
                    role="progressbar"
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={Math.round(analysis.progress * 100)}
                  >
                    <span style={{ width: `${analysis.progress * 100}%` }} />
                  </div>
                </div>

                {analysis.error_message && (
                  <p className="job-error">{analysis.error_message}</p>
                )}

                {analysis.result && (
                  <pre className="result-preview">
                    {JSON.stringify(analysis.result, null, 2)}
                  </pre>
                )}

                <div className="job-footer">
                  <span>{analysis.config.pose_model as string}</span>
                  {canCancel && (
                    <button
                      className="text-button"
                      type="button"
                      onClick={() => void onCancel(analysis.id)}
                      disabled={cancellingId === analysis.id}
                    >
                      {cancellingId === analysis.id ? 'Cancelling…' : 'Cancel job'}
                    </button>
                  )}
                </div>
              </article>
            )
          })}
        </div>
      )}
    </section>
  )
}
