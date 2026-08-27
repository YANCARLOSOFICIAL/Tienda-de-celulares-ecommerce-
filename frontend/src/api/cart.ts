import { Api } from './client'
import type { Product } from './products'

export interface CartItem {
  id: number
  product_id: number
  product: Product
  quantity: number
  subtotal: string
}

export interface Cart {
  id: number
  items: CartItem[]
  total: string
  item_count: number
}

export const cartApi = {
  async get() {
    return Api.get<Cart>('/cart')
  },

  async addItem(productId: number, quantity = 1) {
    return Api.post<CartItem>('/cart/items', { product_id: productId, quantity })
  },

  async updateItem(itemId: number, quantity: number) {
    return Api.patch<CartItem>(`/cart/items/${itemId}`, { quantity })
  },

  async removeItem(itemId: number) {
    return Api.request<{ success: boolean; message: string }>(`/cart/items/${itemId}`, { method: 'DELETE' })
  },

  async clear() {
    return Api.request<{ success: boolean; message: string }>('/cart', { method: 'DELETE' })
  },
}
