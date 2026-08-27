import { Api } from './client'
import type { Product } from './products'

export interface WishlistItem {
  id: number
  product_id: number
  product: Product
  created_at: string
}

export const wishlistApi = {
  async list() {
    return Api.get<WishlistItem[]>('/wishlist')
  },

  async add(productId: number) {
    return Api.request<{ success: boolean; message: string }>(`/wishlist/${productId}`, { method: 'POST' })
  },

  async remove(productId: number) {
    return Api.request<{ success: boolean; message: string }>(`/wishlist/${productId}`, { method: 'DELETE' })
  },
}
