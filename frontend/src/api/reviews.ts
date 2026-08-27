import { Api } from './client'

export interface Review {
  id: number
  user_id: number
  product_id: number
  rating: number
  title: string | null
  comment: string | null
  user_name: string
  created_at: string
}

export interface RatingSummary {
  average: number
  total: number
  distribution: Record<number, number>
}

export interface ReviewPayload {
  product_id: number
  rating: number
  title?: string | null
  comment?: string | null
}

export const reviewsApi = {
  async listForProduct(productId: number) {
    return Api.get<Review[]>(`/reviews/product/${productId}`)
  },

  async getRatingSummary(productId: number) {
    return Api.get<RatingSummary>(`/reviews/product/${productId}/rating`)
  },

  async create(payload: ReviewPayload) {
    return Api.post<Review>('/reviews', payload)
  },

  async update(id: number, payload: Partial<ReviewPayload>) {
    return Api.patch<Review>(`/reviews/${id}`, payload)
  },

  async remove(id: number) {
    return Api.request<{ success: boolean; message: string }>(`/reviews/${id}`, { method: 'DELETE' })
  },
}
