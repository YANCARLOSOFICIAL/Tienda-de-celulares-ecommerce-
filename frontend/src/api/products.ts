import { Api } from './client'
import type { Category } from './categories'

export interface Product {
  id: number
  name: string
  description: string | null
  price: string
  stock: number
  brand: string
  model: string | null
  image: string | null
  is_active: boolean
  category_id: number | null
  category: Category | null
  created_at: string
  updated_at: string
}

export interface ProductPage {
  items: Product[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface ProductFilters {
  search?: string
  category_id?: number
  brand?: string
  min_price?: string
  max_price?: string
  ordering?: string
  page?: number
  page_size?: number
}

export function priceToNumber(price: string): number {
  return Number(price)
}

export function formatPrice(price: string): string {
  return Number(price).toLocaleString('es-MX')
}

export interface ProductPayload {
  name: string
  description?: string | null
  price: string
  stock: number
  brand: string
  model?: string | null
  category_id?: number | null
  image?: string | null
  is_active?: boolean
}

export const productsApi = {
  async list(filters: ProductFilters = {}) {
    const params = new URLSearchParams()
    const entries = Object.entries(filters)
    for (const [key, value] of entries) {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, String(value))
      }
    }
    const query = params.toString()
    return Api.get<ProductPage>(`/products${query ? `?${query}` : ''}`)
  },

  async get(id: number) {
    return Api.get<Product>(`/products/${id}`)
  },

  async create(payload: ProductPayload) {
    return Api.post<Product>('/products', payload)
  },

  async update(id: number, payload: Partial<ProductPayload>) {
    return Api.patch<Product>(`/products/${id}`, payload)
  },

  async remove(id: number) {
    return Api.request<{ success: boolean; message: string }>(`/products/${id}`, { method: 'DELETE' })
  },
}
