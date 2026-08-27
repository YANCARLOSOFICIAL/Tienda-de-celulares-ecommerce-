const API_BASE = import.meta.env.VITE_API_URL ?? '/api'

export class ApiError extends Error {
  status: number
  errors: string[]

  constructor(message: string, status: number, errors: string[] = []) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.errors = errors
  }
}

let authToken: string | null = localStorage.getItem('tiendacell_token')

export function setToken(token: string | null) {
  authToken = token
  if (token) {
    localStorage.setItem('tiendacell_token', token)
  } else {
    localStorage.removeItem('tiendacell_token')
  }
}

export function getToken(): string | null {
  return authToken
}

export function isAuthenticated(): boolean {
  return Boolean(authToken)
}

interface Envelope<T> {
  success: boolean
  message: string
  data: T | null
  errors?: string[]
}

export class Api {
  static async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const isFormBody =
      options.body instanceof FormData || options.body instanceof URLSearchParams
    const headers: Record<string, string> = {
      ...(isFormBody ? {} : { 'Content-Type': 'application/json' }),
      ...(options.headers as Record<string, string> | undefined),
    }
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`
    }

    const response = await fetch(`${API_BASE}${path}`, { ...options, headers })

    const body = (await response.json().catch(() => null)) as Envelope<T> | null

    if (!response.ok) {
      const message = body?.message || `Error del servidor (${response.status})`
      const errors = Array.isArray(body?.errors) ? body.errors : []
      throw new ApiError(message, response.status, errors)
    }

    return body?.data as T
  }

  static get<T>(path: string) {
    return Api.request<T>(path)
  }

  static post<T>(path: string, data?: unknown) {
    return Api.request<T>(path, { method: 'POST', body: data !== undefined ? JSON.stringify(data) : undefined })
  }

  static patch<T>(path: string, data?: unknown) {
    return Api.request<T>(path, { method: 'PATCH', body: data !== undefined ? JSON.stringify(data) : undefined })
  }

  static delete<T>(path: string) {
    return Api.request<T>(path, { method: 'DELETE' })
  }

  /** Descarga binaria autenticada (ej. PDF/XML de facturas). */
  static async download(path: string, fallbackName: string): Promise<{ blob: Blob; filename: string }> {
    const headers: Record<string, string> = {}
    if (authToken) {
      headers['Authorization'] = `Bearer ${authToken}`
    }
    const response = await fetch(`${API_BASE}${path}`, { headers })
    if (!response.ok) {
      const body = (await response.json().catch(() => null)) as Envelope<unknown> | null
      throw new ApiError(body?.message || `Error del servidor (${response.status})`, response.status)
    }
    return {
      blob: await response.blob(),
      filename: Api.getFilename(response.headers.get('Content-Disposition'), fallbackName),
    }
  }

  static getFilename(disposition: string | null, fallback: string): string {
    const match = disposition?.match(/filename="?([^";]+)"?/)
    return match?.[1] ?? fallback
  }

  static login(email: string, password: string) {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return Api.request<{ access_token: string; token_type: string }>('/auth/login', {
      method: 'POST',
      body: form,
    })
  }
}
