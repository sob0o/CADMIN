import type { DesignCreate, DesignDetail, DesignSummary } from './types'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    throw new Error(`API error ${response.status}`)
  }
  return response.json() as Promise<T>
}

export const api = {
  listDesigns: () => request<DesignSummary[]>('/designs'),
  getDesign: (id: number) => request<DesignDetail>(`/designs/${id}`),
  createDesign: (data: DesignCreate) =>
    request<DesignDetail>('/designs', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
}