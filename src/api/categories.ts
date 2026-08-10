import { Api } from './client'

export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
}

export interface CategoryPayload {
  name: string
  description?: string | null
}

export const categoriesApi = {
  async list() {
    return Api.get<Category[]>('/categories')
  },

  async create(payload: CategoryPayload) {
    return Api.post<Category>('/categories', payload)
  },

  async update(id: number, payload: Partial<CategoryPayload>) {
    return Api.patch<Category>(`/categories/${id}`, payload)
  },

  async remove(id: number) {
    return Api.request<{ success: boolean; message: string }>(`/categories/${id}`, { method: 'DELETE' })
  },
}