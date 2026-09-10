const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api').replace(
  /\/$/,
  '',
)

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
  status: 'received' | 'evidence_review' | 'gap_analysis' | 'roadmap' | 'readiness_review'
  status_label: string
  progress_stage: number
  is_demo: boolean
  created_at: string
  updated_at: string
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

export { API_BASE_URL }
