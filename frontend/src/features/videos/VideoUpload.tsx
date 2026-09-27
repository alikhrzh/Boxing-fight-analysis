import { useRef, useState, type ChangeEvent, type DragEvent } from 'react'

import { formatBytes } from '../../lib/format'
import { FilmIcon, UploadIcon, XIcon } from '../../components/Icons'
import type { Video } from '../../types/domain'

const ACCEPTED_EXTENSIONS = ['.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v']

interface VideoUploadProps {
  uploading: boolean
  onUpload: (file: File) => Promise<Video>
}

export function VideoUpload({ uploading, onUpload }: VideoUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [dragging, setDragging] = useState(false)
  const [localError, setLocalError] = useState<string | null>(null)

  function chooseFile(nextFile?: File) {
    setLocalError(null)
    if (!nextFile) return
    const extension = `.${nextFile.name.split('.').pop()?.toLowerCase() ?? ''}`
    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      setLocalError(`Choose a video in ${ACCEPTED_EXTENSIONS.join(', ')} format.`)
      return
    }
    setFile(nextFile)
  }

  function handleInput(event: ChangeEvent<HTMLInputElement>) {
    chooseFile(event.target.files?.[0])
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault()
    setDragging(false)
    chooseFile(event.dataTransfer.files[0])
  }

  async function submit() {
    if (!file) return
    try {
      await onUpload(file)
      setFile(null)
      if (inputRef.current) inputRef.current.value = ''
    } catch {
      // The workspace-level error banner presents API failures.
    }
  }

  return (
    <section className="panel upload-panel" aria-labelledby="upload-heading">
      <div className="panel-heading">
        <span className="eyebrow">Step 01</span>
        <h2 id="upload-heading">Add round footage</h2>
        <p>Upload one continuous round with two visible fighters.</p>
      </div>

      <div
        className={`drop-zone ${dragging ? 'is-dragging' : ''}`}
        onDragEnter={() => setDragging(true)}
        onDragLeave={() => setDragging(false)}
        onDragOver={(event) => event.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          id="video-file"
          type="file"
          accept="video/mp4,video/quicktime,video/webm,video/x-matroska,video/x-msvideo,.m4v"
          onChange={handleInput}
          disabled={uploading}
        />
        <div className="drop-icon"><UploadIcon size={26} /></div>
        <strong>Drop your video here</strong>
        <span>or choose a file from your computer</span>
        <button
          className="button button-secondary"
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
        >
          Browse video
        </button>
      </div>

      {file && (
        <div className="selected-file">
          <span className="file-icon"><FilmIcon /></span>
          <span className="file-details">
            <strong>{file.name}</strong>
            <small>{formatBytes(file.size)}</small>
          </span>
          <button
            type="button"
            className="icon-button"
            onClick={() => setFile(null)}
            aria-label="Remove selected file"
            disabled={uploading}
          >
            <XIcon />
          </button>
        </div>
      )}

      {localError && <p className="field-error" role="alert">{localError}</p>}

      <button
        className="button button-primary button-wide"
        type="button"
        disabled={!file || uploading}
        onClick={() => void submit()}
      >
        {uploading ? 'Uploading…' : 'Upload footage'}
      </button>
      <p className="hint">Accepted formats: MP4, MOV, MKV, WebM, AVI, M4V.</p>
    </section>
  )
}
