import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { App } from './App'

const emptyPagination = { limit: 100, offset: 0, total: 0 }

function jsonResponse(body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('App', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('loads and presents the API workspace', async () => {
    const fetchMock = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        jsonResponse({
          items: [
            {
              id: '5ab9a20b-8afb-4a77-b248-b6dd449078a7',
              original_name: 'sparring-round.mp4',
              content_type: 'video/mp4',
              size_bytes: 1048576,
              sha256: 'a'.repeat(64),
              created_at: '2026-09-26T12:00:00Z',
            },
          ],
          pagination: { ...emptyPagination, total: 1 },
        }),
      )
      .mockResolvedValueOnce(
        jsonResponse({ items: [], pagination: emptyPagination }),
      )
    vi.stubGlobal('fetch', fetchMock)

    render(<App />)

    expect(await screen.findByText(/sparring-round\.mp4/)).toBeInTheDocument()
    expect(screen.getByText('No analysis jobs yet')).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})
