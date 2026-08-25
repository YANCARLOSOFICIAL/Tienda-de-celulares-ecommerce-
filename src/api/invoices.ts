import { Api } from './client'

export type InvoiceStatus = 'PENDING' | 'VALIDATED' | 'FAILED'

export interface Invoice {
  id: number
  order_id: number
  reference_code: string
  bill_number: string | null
  cufe: string | null
  qr_url: string | null
  status: InvoiceStatus
  total: string
  customer_identification: string | null
  error_message: string | null
  validated_at: string | null
  created_at: string
  updated_at: string
}

export interface InvoiceCustomerPayload {
  identification: string
  dv?: number | null
  names?: string | null
  company?: string | null
  trade_name?: string | null
  address?: string | null
  email?: string | null
  phone?: string | null
  /** Códigos DIAN (API v2): 13=Cédula, 31=NIT */
  identification_document_code?: string
  /** 2=Persona Natural, 1=Persona Jurídica */
  legal_organization_code?: string
  /** ZZ=No aplica (consumidor final), 01=IVA */
  tribute_code?: string
  /** Código DANE del municipio */
  municipality_code?: string | null
}

export interface InvoiceCreatePayload {
  customer: InvoiceCustomerPayload
  /** 1=Contado, 2=Crédito */
  payment_form?: '1' | '2'
  /** 10=Efectivo; ver tabla de métodos de pago Factus */
  payment_method_code?: number
  observation?: string | null
  send_email?: boolean
}

export const invoiceStatusLabels: Record<InvoiceStatus, string> = {
  PENDING: 'Pendiente DIAN',
  VALIDATED: 'Validada DIAN',
  FAILED: 'Con error',
}

function triggerBrowserDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

export const invoicesApi = {
  async getForOrder(orderId: number): Promise<Invoice> {
    return Api.get<Invoice>(`/invoices/orders/${orderId}`)
  },

  async create(orderId: number, payload: InvoiceCreatePayload): Promise<Invoice> {
    return Api.post<Invoice>(`/invoices/orders/${orderId}`, payload)
  },

  async remove(orderId: number): Promise<void> {
    await Api.delete(`/invoices/orders/${orderId}`)
  },

  async downloadPdf(billNumber: string) {
    const { blob, filename } = await Api.download(
      `/invoices/${encodeURIComponent(billNumber)}/pdf`,
      `${billNumber}.pdf`,
    )
    triggerBrowserDownload(blob, filename)
  },

  async downloadXml(billNumber: string) {
    const { blob, filename } = await Api.download(
      `/invoices/${encodeURIComponent(billNumber)}/xml`,
      `${billNumber}.xml`,
    )
    triggerBrowserDownload(blob, filename)
  },
}
