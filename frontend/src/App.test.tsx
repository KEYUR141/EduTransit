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
        if (url.endsWith('/support-cases/1/analyse/')) {
          const analysis = {
            query: 'B.Pharm to data science',
            scenario_id: null,
            discovery_mode: true,
            matched_scenario: {
              scenario_id: 'S021',
              title: 'Pharmacy to data science transition',
              rarity: 'uncommon',
            },
            confidence: {
              score: 0.58,
              level: 'medium',
              top_result_score: 0.72,
              matched_term_coverage: 0.6,
              supporting_chunks: 3,
              discovery_margin: 0.12,
              explanation: 'Useful evidence exists, but an instructor should review it.',
              is_eligibility_probability: false,
            },
            review: {
              required: true,
              route: 'instructor_review',
              priority: 'normal',
              reason_codes: ['limited_query_term_coverage'],
              publication_status: 'provisional',
            },
            count: 1,
            results: [
              {
                chunk_id: 's021-statistics',
                score: 0.72,
                lexical_score: 0.7,
                vector_score: 0.74,
                matched_terms: ['statistics', 'probability'],
                retrieval_reasons: ['matched canonical terms'],
                text: 'The learner completed an undergraduate biostatistics course.',
                section: 'learner_evidence',
                citation: {
                  source_id: 'fixture-s021',
                  title: 'Reviewed pharmacy transition evidence',
                  organisation: 'GapMap prototype dataset',
                  url: '',
                  version: '2026-demo',
                  review_status: 'reviewed',
                },
              },
            ],
          }
          return jsonResponse({
            case: {
              ...demoCase,
              status: 'instructor_review',
              status_label: 'Instructor review',
              progress_stage: 2,
              analysis_confidence_score: 0.58,
              analysis_confidence_level: 'medium',
              review_required: true,
              review_route: 'instructor_review',
              analysis_snapshot: analysis,
              analysed_at: '2026-09-11T01:00:00Z',
            },
            analysis,
          })
        }        if (init?.method === 'POST') {
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

  it('runs backend evidence analysis and renders its review data', async () => {
    render(<App />)

    await screen.findByText(/system available/i)
    const analysisButtons = screen.getAllByRole('button', { name: /generate evidence report/i })
    fireEvent.click(analysisButtons.at(-1)!)

    expect(await screen.findByText('58%')).toBeInTheDocument()
    expect(screen.getByRole('tab', { name: /full report \(1\)/i })).toBeInTheDocument()
    expect(screen.getByText(/reviewed pharmacy transition evidence/i)).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/support-cases\/1\/analyse\/$/),
      expect.objectContaining({ method: 'POST' }),
    )
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