import { fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import App from './App'
import type { SupportCase } from './api'

const demoCase: SupportCase = {
  id: 1,
  reference: 'GM-2048',
  title: 'B.Pharm to Master of Data Science',
  requester_name: 'Ananya Rao',
  requester_role: 'student',
  category: 'study-abroad',
  category_label: 'Study-abroad preparation',
  summary: 'Understand academic readiness for a Master of Data Science programme.',
  source_label: 'PCI B.Pharm',
  source_location: 'India',
  destination_label: 'Master of Data Science',
  destination_location: 'UBC, Canada',
  status: 'gap_analysis',
  status_label: 'Gap comparison',
  progress_stage: 3,
  is_demo: true,
  created_at: '2026-09-11T00:00:00Z',
  updated_at: '2026-09-11T00:00:00Z',
}

const jsonResponse = (body: unknown) =>
  ({ ok: true, json: async () => body }) as Response

describe('GapMap learner support workspace', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input)
        if (url.endsWith('/health/')) {
          return jsonResponse({ status: 'ok', service: 'GapMap API', time: '2026-09-11T00:00:00Z' })
        }
        if (init?.method === 'POST') {
          return jsonResponse({
            ...demoCase,
            id: 2,
            reference: 'GM-NEW123',
            title: 'Previous programme to Destination programme',
            status: 'received',
            status_label: 'Request received',
            progress_stage: 1,
            is_demo: false,
          })
        }
        return jsonResponse({ count: 1, results: [demoCase] })
      }),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('loads support choices and an active learner case from the API', async () => {
    render(<App />)

    expect(
      screen.getByRole('heading', {
        name: /find what is missing.*keep what you already know/i,
      }),
    ).toBeInTheDocument()
    expect(screen.getAllByText(/support directory/i)).toHaveLength(2)
    expect(await screen.findByText(/case gm-2048/i)).toBeInTheDocument()
    expect(await screen.findByText(/system available/i)).toBeInTheDocument()
  })

  it('creates a support request through the API', async () => {
    render(<App />)

    fireEvent.click(screen.getAllByRole('button', { name: /raise a support request/i })[0])
    fireEvent.change(screen.getByLabelText(/current school or programme/i), {
      target: { value: 'Previous programme' },
    })
    fireEvent.change(screen.getByLabelText(/destination goal/i), {
      target: { value: 'Destination programme' },
    })
    fireEvent.change(screen.getByLabelText(/briefly describe the difficulty/i), {
      target: { value: 'I changed programmes and do not know which prerequisites I am missing.' },
    })
    fireEvent.click(screen.getByRole('button', { name: /create support request/i }))

    expect(await screen.findByText(/request created/i)).toBeInTheDocument()
    expect(screen.getByText('GM-NEW123')).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/support-cases\/$/),
      expect.objectContaining({ method: 'POST' }),
    )
  })
})