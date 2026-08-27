import { Api } from './client'

export interface Role {
  id: number
  name: string
}

export interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  role: Role
  created_at: string
  updated_at: string
}

export interface RegisterPayload {
  email: string
  full_name: string
  password: string
}

export const authApi = {
  async register(payload: RegisterPayload) {
    return Api.post<{ id: number; email: string; full_name: string }>('/auth/register', payload)
  },

  async login(email: string, password: string) {
    return Api.login(email, password)
  },

  async me() {
    return Api.get<User>('/users/me')
  },

  async updateProfile(payload: { full_name?: string; password?: string }) {
    return Api.patch<User>('/users/me', payload)
  },
}
