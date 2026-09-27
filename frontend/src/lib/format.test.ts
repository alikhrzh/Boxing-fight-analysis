import { describe, expect, it } from 'vitest'

import { formatBytes, shortId } from './format'

describe('formatBytes', () => {
  it('formats byte values with an appropriate unit', () => {
    expect(formatBytes(0)).toBe('0 B')
    expect(formatBytes(1536)).toBe('1.5 KB')
    expect(formatBytes(12 * 1024 * 1024)).toBe('12 MB')
  })
})

describe('shortId', () => {
  it('returns the first eight characters', () => {
    expect(shortId('12345678-abcd-efgh')).toBe('12345678')
  })
})
