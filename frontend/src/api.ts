const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api').replace(
  /\/$/,
  '',
)

export type ConfidenceLevel = 'not_analysed' | 'low' | 'medium' | 'high'
export type ReviewRoute =
  | 'not_routed'
  | 'provisional_guidance'
  | 'instructor_review'
  | 'specialist_escalation'

export type SupportCase = {
  id: number
  reference: string
  title: string
  requester_name: string
  requester_role: 'student' | 'parent' | 'educator'
  category: string
  category_label: string
  summary: string
  source_label: string
  source_location: string
  destination_label: string
  destination_location: string
  status:
    | 'received'
    | 'evidence_review'
    | 'gap_analysis'
    | 'roadmap'
    | 'readiness_review'
    | 'instructor_review'
  status_label: string
  progress_stage: number
  matched_scenario?: number | null
  analysis_confidence_score?: number | null
  analysis_confidence_level?: ConfidenceLevel
  review_required?: boolean
  review_route?: ReviewRoute
  analysis_snapshot?: RagAnalysis | Record<string, never>
  analysed_at?: string | null
  is_demo: boolean
  created_at: string
  updated_at: string
}

export type RagResult = {
  chunk_id: string
  score: number
  lexical_score: number
  vector_score: number
  matched_terms: string[]
  retrieval_reasons: string[]
  text: string
  section: string
  page?: number | null
  metadata: Record<string, unknown>
  citation: {
    source_id: string
    title: string
    organisation: string
    url: string
    version: string
    review_status: string
  }
}

export type RagAnalysis = {
  query: string
  scenario_id: string | null
  discovery_mode: boolean
  matched_scenario: {
    scenario_id: string
    title: string
    rarity: string
  } | null
  confidence: {
    score: number
    level: 'low' | 'medium' | 'high'
    top_result_score: number
    matched_term_coverage: number
    supporting_chunks: number
    discovery_margin: number
    explanation: string
    is_eligibility_probability: boolean
  }
  review: {
    required: boolean
    route: ReviewRoute
    priority: string
    reason_codes: string[]
    publication_status: string
  }
  count: number
  results: RagResult[]
}

export type CreateSupportCase = {
  title: string
  requester_name: string
  requester_role: SupportCase['requester_role']
  category: string
  summary: string
  source_label: string
  source_location: string
  destination_label: string
  destination_location: string
}

type PaginatedResponse<T> = {
  count: number
  results: T[]
}

async function readJson<T>(response: Response): Promise<T> {
  const body = await response.json()
  if (!response.ok) {
    const message =
      typeof body?.detail === 'string'
        ? body.detail
        : Object.values(body ?? {}).flat().join(' ') || 'The request could not be completed.'
    throw new Error(message)
  }
  return body as T
}

export async function checkApiHealth(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/health/`, {
    headers: { Accept: 'application/json' },
  })
  await readJson(response)
}

export async function listSupportCases(): Promise<SupportCase[]> {
  const response = await fetch(`${API_BASE_URL}/support-cases/?ordering=-updated_at`, {
    headers: { Accept: 'application/json' },
  })
  const body = await readJson<PaginatedResponse<SupportCase>>(response)
  return body.results
}

export async function createSupportCase(payload: CreateSupportCase): Promise<SupportCase> {
  const response = await fetch(`${API_BASE_URL}/support-cases/`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
  return readJson<SupportCase>(response)
}

export async function analyseSupportCase(id: number): Promise<{
  case: SupportCase
  analysis: RagAnalysis
}> {
  const response = await fetch(`${API_BASE_URL}/support-cases/${id}/analyse/`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ top_k: 5 }),
  })
  return readJson(response)
}

export { API_BASE_URL }

export type EmbeddingMapPoint = {
  chunk_id: string
  x: number
  y: number
  z: number
  section: string
  review_status: string
  scenario: { scenario_id: string; title: string; rarity: string } | null
}

export type EmbeddingMapResponse = {
  projection: string
  source_dimensions: number
  dimensions: number
  embedding_model: string
  count: number
  explained_variance: number[]
  points: EmbeddingMapPoint[]
}

export async function getEmbeddingMap(maxPoints = 300): Promise<EmbeddingMapResponse> {
  const response = await fetch(`${API_BASE_URL}/rag/embedding-map/?max_points=${maxPoints}`, {
    headers: { Accept: 'application/json' },
  })
  return readJson<EmbeddingMapResponse>(response)
}