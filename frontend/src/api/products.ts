import { Api } from './client'
import { formatNumber } from '@/config/site'
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
  images: string[]
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
  /** Uno o varios IDs de categoría (se envían como `category_id` repetido). */
  category_id?: number[]
  /** Una o varias marcas (se envían como `brand` repetido). */
  brand?: string[]
  min_price?: string
  max_price?: string
  ordering?: string
  page?: number
  page_size?: number
}

export function priceToNumber(price: string): number {
  return Number(price)
}

/** Precio agrupado en formato colombiano, sin decimales. Las plantillas anteponen "$". */
export function formatPrice(price: string | number): string {
  return formatNumber(price)
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
  images?: string[]
  is_active?: boolean
}

export const productsApi = {
  async list(filters: ProductFilters = {}) {
    const params = new URLSearchParams()
    for (const [key, value] of Object.entries(filters)) {
      if (value === undefined || value === null || value === '') continue
      if (Array.isArray(value)) {
        for (const v of value) {
          if (v !== undefined && v !== null && v !== '') params.append(key, String(v))
        }
      } else {
        params.append(key, String(value))
      }
    }
    const query = params.toString()
    return Api.get<ProductPage>(`/products${query ? `?${query}` : ''}`)
  },

  async brands() {
    return Api.get<string[]>('/products/brands')
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
