import { Api } from './client'

export interface AdminStats {
  total_orders: number
  total_revenue: string
  total_products: number
  total_users: number
  orders_by_status: Record<string, number>
  recent_orders: { id: number; status: string; total: string; created_at: string }[]
  top_products: { name: string; total_sold: number; total_revenue: string }[]
}

export const adminApi = {
  async getStats() {
    return Api.get<AdminStats>('/admin/stats')
  },
}
