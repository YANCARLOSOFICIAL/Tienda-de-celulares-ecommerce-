<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { PackageOpen, Pencil, ChevronDown, ChevronUp, FileText, Download } from '@lucide/vue'

import { ordersApi, orderStatusLabels, type Order, type OrderStatus } from '@/api/orders'
import { formatPrice } from '@/api/products'
import {
  invoicesApi,
  invoiceStatusLabels,
  type Invoice,
  type InvoiceCreatePayload,
  type InvoiceStatus,
} from '@/api/invoices'

const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const banner = ref<string | null>(null)

const editingId = ref<number | null>(null)
const editingStatus = ref<OrderStatus>('PENDING')
const formBusy = ref(false)
const expandedId = ref<number | null>(null)

// Facturación electrónica
const invoicesByOrder = ref<Record<number, Invoice | null>>({})
const invoicingOrderId = ref<number | null>(null)
const invoiceBusy = ref(false)
const invoiceForm = reactive<InvoiceCreatePayload>({
  customer: { identification: '', names: '', email: '', phone: '', address: '' },
})

const statusOptions = Object.keys(orderStatusLabels) as OrderStatus[]

const statusBadgeMap: Record<string, string> = {
  PENDING: 'badge-warning',
  CONFIRMED: 'badge-accent',
  SHIPPED: 'badge-accent',
  DELIVERED: 'badge-success',
  CANCELLED: 'badge-danger',
}

const invoiceBadgeMap: Record<InvoiceStatus, string> = {
  PENDING: 'badge-warning',
  VALIDATED: 'badge-success',
  FAILED: 'badge-danger',
}

async function load() {
  loading.value = true
  error.value = null
  try {
    orders.value = await ordersApi.list()
    invoicesByOrder.value = {}
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar pedidos.'
  } finally {
    loading.value = false
  }
}

function openEdit(order: Order) {
  editingId.value = order.id
  editingStatus.value = order.status
}

async function saveStatus() {
  if (editingId.value === null) return
  formBusy.value = true
  error.value = null
  try {
    const updated = await ordersApi.updateStatus(editingId.value, editingStatus.value)
    const idx = orders.value.findIndex((o) => o.id === updated.id)
    if (idx !== -1) orders.value[idx] = updated
    banner.value = 'Estado del pedido actualizado correctamente.'
    editingId.value = null
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al actualizar el estado.'
  } finally {
    formBusy.value = false
  }
}

function toggleExpand(orderId: number) {
  expandedId.value = expandedId.value === orderId ? null : orderId
  if (expandedId.value === orderId) void ensureInvoice(orderId)
}

async function ensureInvoice(orderId: number) {
  if (orderId in invoicesByOrder.value) return
  invoicesByOrder.value[orderId] = await invoicesApi.getForOrder(orderId).catch(() => null)
}

function openInvoiceForm(order: Order) {
  invoicingOrderId.value = order.id
  invoiceForm.customer.identification = ''
  invoiceForm.customer.names = ''
  invoiceForm.customer.email = ''
  invoiceForm.customer.phone = ''
  invoiceForm.customer.address = ''
}

async function emitInvoice(order: Order) {
  if (!invoiceForm.customer.identification.trim()) {
    error.value = 'La identificación del cliente es obligatoria para facturar.'
    return
  }
  invoiceBusy.value = true
  error.value = null
  try {
    const created = await invoicesApi.create(order.id, { customer: { ...invoiceForm.customer } })
    invoicesByOrder.value[order.id] = created
    invoicingOrderId.value = null
    banner.value =
      created.status === 'VALIDATED'
        ? `Factura ${created.bill_number} emitida y validada por la DIAN.`
        : `Factura registrada (pendiente de validación DIAN).`
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al emitir la factura.'
    void ensureInvoiceRefresh(order.id)
  } finally {
    invoiceBusy.value = false
  }
}

async function ensureInvoiceRefresh(orderId: number) {
  delete invoicesByOrder.value[orderId]
  await ensureInvoice(orderId)
}

async function downloadInvoice(kind: 'pdf' | 'xml', billNumber: string | null) {
  if (!billNumber) return
  try {
    if (kind === 'pdf') await invoicesApi.downloadPdf(billNumber)
    else await invoicesApi.downloadXml(billNumber)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al descargar la factura.'
  }
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('es-CO', { dateStyle: 'short', timeStyle: 'short' })
}

onMounted(load)
</script>

<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-text flex items-center gap-2" style="font-family: var(--font-family-serif);">
        <PackageOpen :size="24" :stroke-width="2" />
        Pedidos
      </h2>
      <p class="text-sm text-text-secondary">Consulta todos los pedidos y actualiza su estado.</p>
    </div>

    <p v-if="banner" class="badge-success px-4 py-2 text-sm font-medium">{{ banner }}</p>
    <p v-if="error" class="badge-danger px-4 py-2 text-sm font-medium">{{ error }}</p>

    <div v-if="loading" class="bento-card-static glass p-8">
      <div class="space-y-4">
        <div v-for="i in 4" :key="i" class="flex items-center gap-4">
          <div class="skeleton h-4 w-24"></div>
          <div class="skeleton h-4 flex-1"></div>
          <div class="skeleton h-4 w-16"></div>
        </div>
      </div>
    </div>

    <div v-else-if="orders.length === 0" class="bento-card-static glass p-12 text-center">
      <PackageOpen :size="40" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-3" />
      <p class="text-lg font-semibold text-text">Sin pedidos</p>
      <p class="text-sm text-text-secondary mt-1">No hay pedidos registrados.</p>
    </div>

    <div v-else class="bento-card-static glass overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border-light">
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Pedido</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Cliente</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Fecha</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Estado</th>
              <th class="text-right px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Total</th>
              <th class="text-right px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="order in orders" :key="order.id">
              <tr class="border-b border-border-light last:border-b-0 admin-table-row">
                <td class="px-4 py-3 font-medium text-text">#{{ order.id }}</td>
                <td class="px-4 py-3 text-text-secondary">Usuario #{{ order.user_id }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ formatDate(order.created_at) }}</td>
                <td class="px-4 py-3">
                  <span :class="['badge text-xs', statusBadgeMap[order.status] || 'badge']">
                    {{ orderStatusLabels[order.status] }}
                  </span>
                </td>
                <td class="px-4 py-3 text-right font-semibold text-text">${{ formatPrice(order.total) }}</td>
                <td class="px-4 py-3">
                  <div class="flex gap-1 justify-end">
                    <button class="p-2 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors" title="Expandir" @click="toggleExpand(order.id)">
                      <ChevronUp v-if="expandedId === order.id" :size="16" :stroke-width="2" />
                      <ChevronDown v-else :size="16" :stroke-width="2" />
                    </button>
                    <button class="p-2 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors" title="Cambiar estado" @click="openEdit(order)">
                      <Pencil :size="16" :stroke-width="2" />
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="expandedId === order.id" class="bg-surface-dim/50 border-b border-border-light">
                <td colspan="6" class="px-4 py-4">
                  <div class="space-y-3">
                    <div>
                      <p class="text-xs font-medium text-text-secondary uppercase tracking-wider mb-2">Artículos</p>
                      <div class="space-y-1.5">
                        <div v-for="item in order.items" :key="item.id" class="flex justify-between text-sm">
                          <span class="text-white">{{ item.quantity }} × {{ item.product_name }}</span>
                          <span class="font-medium text-text">${{ formatPrice(item.subtotal) }}</span>
                        </div>
                      </div>
                    </div>
                    <div class="divider"></div>
                    <div class="flex items-center justify-between">
                      <span class="text-sm font-medium text-text-secondary">Total</span>
                      <span class="text-lg font-bold text-text">${{ formatPrice(order.total) }}</span>
                    </div>

                    <!-- Facturación electrónica (Factus) -->
                    <div class="pt-2 space-y-2">
                      <p class="text-xs font-medium text-text-secondary uppercase tracking-wider">Facturación electrónica</p>

                      <div v-if="invoicesByOrder[order.id]" class="flex flex-wrap items-center gap-3 text-sm">
                        <FileText :size="16" :stroke-width="2" class="text-accent" />
                        <span class="font-medium text-text">{{ invoicesByOrder[order.id]?.bill_number || 'Sin número' }}</span>
                        <span :class="['badge text-xs', invoiceBadgeMap[invoicesByOrder[order.id]!.status]]">
                          {{ invoiceStatusLabels[invoicesByOrder[order.id]!.status] }}
                        </span>
                        <button
                          v-if="invoicesByOrder[order.id]?.bill_number"
                          class="btn-ghost text-xs inline-flex items-center gap-1"
                          @click="downloadInvoice('pdf', invoicesByOrder[order.id]?.bill_number ?? null)"
                        >
                          <Download :size="12" :stroke-width="2" /> PDF
                        </button>
                        <button
                          v-if="invoicesByOrder[order.id]?.bill_number"
                          class="btn-ghost text-xs inline-flex items-center gap-1"
                          @click="downloadInvoice('xml', invoicesByOrder[order.id]?.bill_number ?? null)"
                        >
                          <Download :size="12" :stroke-width="2" /> XML
                        </button>
                      </div>

                      <div v-else-if="invoicingOrderId === order.id" class="space-y-2">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          <input v-model="invoiceForm.customer.identification" class="input-minimal" placeholder="Identificación (CC/NIT) *" />
                          <input v-model="invoiceForm.customer.names" class="input-minimal" placeholder="Nombre / Razón social" />
                          <input v-model="invoiceForm.customer.email" type="email" class="input-minimal" placeholder="Correo electrónico" />
                          <input v-model="invoiceForm.customer.phone" class="input-minimal" placeholder="Teléfono" />
                          <input v-model="invoiceForm.customer.address" class="input-minimal sm:col-span-2" placeholder="Dirección" />
                        </div>
                        <div class="flex gap-2 justify-end">
                          <button class="btn-secondary text-xs" @click="invoicingOrderId = null">
                            Cancelar
                          </button>
                          <button :disabled="invoiceBusy" class="btn-primary text-xs disabled:opacity-50" @click="emitInvoice(order)">
                            {{ invoiceBusy ? 'Emitiendo...' : 'Emitir factura' }}
                          </button>
                        </div>
                      </div>

                      <button
                        v-else-if="order.status !== 'CANCELLED'"
                        class="btn-ghost text-sm w-full flex items-center justify-center gap-2"
                        @click="openInvoiceForm(order)"
                      >
                        <FileText :size="14" :stroke-width="2" />
                        Emitir factura electrónica
                      </button>

                      <p v-else class="text-xs text-text-tertiary">
                        Los pedidos cancelados no pueden facturarse.
                      </p>
                    </div>

                    <div v-if="editingId === order.id" class="pt-2 space-y-2">
                      <label class="block text-sm font-medium text-text-secondary">Nuevo estado</label>
                      <select v-model="editingStatus" class="input-minimal">
                        <option v-for="status in statusOptions" :key="status" :value="status">{{ orderStatusLabels[status] }}</option>
                      </select>
                      <div class="flex gap-2 justify-end">
                        <button class="btn-secondary text-xs" @click="editingId = null">
                          Cancelar
                        </button>
                        <button :disabled="formBusy" class="btn-primary text-xs disabled:opacity-50" @click="saveStatus">
                          {{ formBusy ? 'Guardando...' : 'Guardar estado' }}
                        </button>
                      </div>
                    </div>
                    <button
                      v-else
                      class="btn-ghost text-sm w-full flex items-center justify-center gap-2"
                      @click="openEdit(order)"
                    >
                      <Pencil :size="14" :stroke-width="2" />
                      Cambiar estado
                    </button>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
