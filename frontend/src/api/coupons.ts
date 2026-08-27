import { Api } from './client'

export interface Coupon {
  id: number
  code: string
  discount_type: string
  discount_value: string
  min_purchase: string
  max_uses: number | null
  used_count: number
  expires_at: string | null
  is_active: boolean
  created_at: string
}

export interface CouponPayload {
  code: string
  discount_type: 'PERCENTAGE' | 'FIXED'
  discount_value: number
  min_purchase?: number
  max_uses?: number | null
  expires_at?: string | null
}

export interface CouponValidateResult {
  id: number
  code: string
  discount_type: string
  discount_value: string
  min_purchase: string
}

export const couponsApi = {
  async list() {
    return Api.get<Coupon[]>('/coupons')
  },

  async get(id: number) {
    return Api.get<Coupon>(`/coupons/${id}`)
  },

  async create(payload: CouponPayload) {
    return Api.post<Coupon>('/coupons', payload)
  },

  async update(id: number, payload: Partial<CouponPayload & { is_active: boolean }>) {
    return Api.patch<Coupon>(`/coupons/${id}`, payload)
  },

  async remove(id: number) {
    return Api.request<{ success: boolean; message: string }>(`/coupons/${id}`, { method: 'DELETE' })
  },

  async validate(code: string, subtotal: number) {
    return Api.post<CouponValidateResult>('/coupons/validate?code=' + encodeURIComponent(code) + '&subtotal=' + subtotal)
  },
}
