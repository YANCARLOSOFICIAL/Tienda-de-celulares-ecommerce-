import { Api } from './client'

export interface Address {
  id: number
  user_id: number
  label: string
  full_name: string
  phone: string
  street: string
  street_number: string | null
  interior: string | null
  neighborhood: string
  city: string
  state: string
  zip_code: string
  is_default: boolean
  created_at: string
  updated_at: string
}

export interface AddressPayload {
  label?: string
  full_name: string
  phone: string
  street: string
  street_number?: string | null
  interior?: string | null
  neighborhood: string
  city: string
  state: string
  zip_code: string
  is_default?: boolean
}

export const addressesApi = {
  async list() {
    return Api.get<Address[]>('/addresses')
  },

  async get(id: number) {
    return Api.get<Address>(`/addresses/${id}`)
  },

  async create(payload: AddressPayload) {
    return Api.post<Address>('/addresses', payload)
  },

  async update(id: number, payload: Partial<AddressPayload>) {
    return Api.patch<Address>(`/addresses/${id}`, payload)
  },

  async remove(id: number) {
    return Api.request<{ success: boolean; message: string }>(`/addresses/${id}`, { method: 'DELETE' })
  },
}
