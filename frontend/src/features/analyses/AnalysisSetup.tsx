import { useEffect, useState, type FormEvent } from 'react'

import { ArrowIcon } from '../../components/Icons'
import { formatBytes } from '../../lib/format'
import type { Analysis, CreateAnalysisInput, Video } from '../../types/domain'

interface AnalysisSetupProps {
  videos: Video[]
  selectedVideoId: string
  creating: boolean
  onSelectedVideoChange: (id: string) => void
  onCreate: (input: CreateAnalysisInput) => Promise<Analysis>
}

export function AnalysisSetup({
  videos,
  selectedVideoId,
  creating,
  onSelectedVideoChange,
  onCreate,
}: AnalysisSetupProps) {
  const [roundNumber, setRoundNumber] = useState(1)
  const [poseModel, setPoseModel] = useState('yolo11s-pose')

  useEffect(() => {
    if (!selectedVideoId && videos[0]) onSelectedVideoChange(videos[0].id)
  }, [onSelectedVideoChange, selectedVideoId, videos])

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!selectedVideoId) return
    try {
      await onCreate({
        video_id: selectedVideoId,
        round_number: roundNumber,
        config: { pose_model: poseModel },
      })
    } catch {
      // The workspace-level error banner presents API failures.
    }
  }

  return (
    <section className="panel setup-panel" aria-labelledby="setup-heading">
      <div className="panel-heading">
        <span className="eyebrow">Step 02</span>
        <h2 id="setup-heading">Configure analysis</h2>
        <p>Create a reproducible job from uploaded footage.</p>
      </div>

      {videos.length === 0 ? (
        <div className="empty-setup">
          <span>01</span>
          <h3>Footage comes first</h3>
          <p>Upload a boxing round to unlock analysis settings.</p>
        </div>
      ) : (
        <form className="setup-form" onSubmit={(event) => void submit(event)}>
          <label>
            <span>Source video</span>
            <select
              value={selectedVideoId}
              onChange={(event) => onSelectedVideoChange(event.target.value)}
              required
            >
              {videos.map((video) => (
                <option key={video.id} value={video.id}>
                  {video.original_name} · {formatBytes(video.size_bytes)}
                </option>
              ))}
            </select>
          </label>

          <div className="form-row">
            <label>
              <span>Round number</span>
              <input
                type="number"
                min="1"
                max="99"
                value={roundNumber}
                onChange={(event) => setRoundNumber(event.target.valueAsNumber)}
                required
              />
            </label>
            <label>
              <span>Pose model</span>
              <select
                value={poseModel}
                onChange={(event) => setPoseModel(event.target.value)}
              >
                <option value="yolo11s-pose">YOLO 11 Small · faster</option>
                <option value="yolo11m-pose">YOLO 11 Medium · precise</option>
              </select>
            </label>
          </div>

          <div className="notice">
            <strong>Worker integration pending</strong>
            <p>
              The job will be safely queued. Vision processing starts once the
              analysis worker is connected.
            </p>
          </div>

          <button
            className="button button-primary button-wide"
            type="submit"
            disabled={creating || !selectedVideoId}
          >
            {creating ? 'Creating job…' : 'Queue analysis'}
            {!creating && <ArrowIcon />}
          </button>
        </form>
      )}
    </section>
  )
}
