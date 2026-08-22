import { Api } from './client'

export type OrderStatus =
  | 'PENDING'
  | 'CONFIRMED'
  | 'PROCESSING'
  | 'SHIPPED'
  | 'DELIVERED'
  | 'CANCELLED'

export interface OrderItem {
  id: number
  product_id: number | null
  product_name: string
  unit_price: string
  quantity: number
  subtotal: string
}

export interface Order {
  id: number
  status: OrderStatus
  total: string
  user_id: number
  items: OrderItem[]
  created_at: string
  updated_at: string
}

export const orderStatusLabels: Record<OrderStatus, string> = {
  PENDING: 'Pendiente',
  CONFIRMED: 'Confirmado',
  PROCESSING: 'En preparación',
  SHIPPED: 'Enviado',
  DELIVERED: 'Entregado',
  CANCELLED: 'Cancelado',
}

export interface OrderCreatePayload {
  address_id?: number | null
  shipping_method?: string
  notes?: string | null
}

export const ordersApi = {
  async create(payload?: OrderCreatePayload) {
    return Api.post<Order>('/orders', payload)
  },

  async list() {
    return Api.get<Order[]>('/orders')
  },

  async get(id: number) {
    return Api.get<Order>(`/orders/${id}`)
  },

  async updateStatus(id: number, status: OrderStatus) {
    return Api.patch<Order>(`/orders/${id}/status`, { status })
  },
}
