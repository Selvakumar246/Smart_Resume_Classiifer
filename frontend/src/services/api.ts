import type { AnalysisDetail, AnalysisSummary, AuthResponse, DashboardData, User } from '../types'

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

function token() {
  return localStorage.getItem('resume_ai_token')
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers)
  if (!(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  const authToken = token()
  if (authToken) headers.set('Authorization', `Bearer ${authToken}`)
  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Something went wrong.' }))
    throw new Error(payload.detail || `Request failed with ${response.status}`)
  }
  if (response.status === 204) return undefined as T
  return response.json()
}

export const api = {
  register: (name: string, email: string, password: string) => request<AuthResponse>('/auth/register', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
  sendFeedback: (payload: { name: string; email: string; subject: string; message: string; rating?: number }) => request<{ message: string }>('/feedback', { method: 'POST', body: JSON.stringify(payload) }),
  login: (email: string, password: string, remember_me = false) => request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password, remember_me }) }),
  firebaseAuth: (idToken: string) => request<AuthResponse>('/auth/firebase', { method: 'POST', body: JSON.stringify({ id_token: idToken }) }),
  forgotPassword: (email: string) => request<{ message: string; reset_token?: string }>('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
  resetPassword: (token: string, password: string) => request<{ message: string }>('/auth/reset-password', { method: 'POST', body: JSON.stringify({ token, password }) }),
  me: () => request<User>('/users/me'),
  dashboard: () => request<DashboardData>('/dashboard'),
  adminOverview: () => request<{ users: number; analyses: number; feedback: number; average_ats: number; system_health: string; model: string; accuracy_note: string }>('/admin/overview'),
  analyses: () => request<AnalysisSummary[]>('/analyses'),
  analysis: (id: string) => request<AnalysisDetail>(`/analyses/${id}`),
  createAnalysis: (form: FormData) => request<AnalysisDetail>('/analyses', { method: 'POST', body: form }),
  deleteAnalysis: (id: string) => request<void>(`/analyses/${id}`, { method: 'DELETE' }),
  reportUrl: (id: string) => `${API_URL}/analyses/${id}/report`,
  googleLoginUrl: `${API_URL}/auth/google/login`,
}

export async function downloadReport(id: string, filename = 'smart-resume-report.pdf') {
  const response = await fetch(api.reportUrl(id), { headers: { Authorization: `Bearer ${token()}` } })
  if (!response.ok) throw new Error('Could not generate the report.')
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}
