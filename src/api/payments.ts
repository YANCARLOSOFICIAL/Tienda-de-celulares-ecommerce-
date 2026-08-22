import { Api } from './client'

export interface Payment {
  id: number
  order_id: number
  external_id: string | null
  payment_method: string | null
  status: string
  amount: string
  currency: string
  checkout_url: string | null
}

export const paymentStatusLabel: Record<string, string> = {
  PENDING: 'Pendiente',
  APPROVED: 'Aprobado',
  REJECTED: 'Rechazado',
  CANCELLED: 'Cancelado',
  REFUNDED: 'Reembolsado',
}

export const paymentsApi = {
  async create(orderId: number) {
    return Api.post<{ payment_id: number; checkout_url: string | null; preference_id: string | null }>(
      `/payments/create/${orderId}`,
    )
  },

  async getByOrder(orderId: number) {
    return Api.get<Payment>(`/payments/order/${orderId}`)
  },

  async confirm(paymentId: number) {
    return Api.post<Payment>(`/payments/confirm/${paymentId}`)
  },
}
