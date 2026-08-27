<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Package, FileText, Download } from '@lucide/vue'

import { formatPrice } from '@/api/products'
import { ordersApi, orderStatusLabels, type Order } from '@/api/orders'
import { invoicesApi } from '@/api/invoices'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const downloadingOrderId = ref<number | null>(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/orders' } })
    return
  }
  await loadOrders()
})

async function loadOrders() {
  loading.value = true
  error.value = null
  try {
    orders.value = await ordersApi.list()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar los pedidos.'
  } finally {
    loading.value = false
  }
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

async function downloadInvoicePdf(order: Order) {
  if (!order.invoice?.bill_number) return
  downloadingOrderId.value = order.id
  try {
    await invoicesApi.downloadPdf(order.invoice.bill_number)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al descargar la factura.'
  } finally {
    downloadingOrderId.value = null
  }
}

const statusBadge: Record<string, string> = {
  PENDING: 'badge-warning',
  CONFIRMED: 'badge-accent',
  PROCESSING: 'badge-accent',
  SHIPPED: 'badge-warning',
  DELIVERED: 'badge-success',
  CANCELLED: 'badge-danger',
}
</script>

<template>
  <section class="py-16 sm:py-20 min-h-[70vh]">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <Package :size="20" :stroke-width="2" class="text-text-secondary" />
        <h1 class="text-2xl sm:text-3xl font-semibold text-white" style="font-family: var(--font-family-serif);">Mis pedidos</h1>
      </div>

      <div v-if="loading" class="bg-surface-dim border border-border rounded-2xl p-10 text-center">
        <div class="skeleton h-5 w-48 mx-auto mb-3"></div>
        <div class="skeleton h-4 w-32 mx-auto"></div>
      </div>

      <div v-else-if="error" class="bg-surface-dim border border-border rounded-2xl p-10 text-center">
        <p class="text-sm text-text-secondary">{{ error }}</p>
        <button class="btn-secondary mt-4 text-sm" @click="loadOrders">Reintentar</button>
      </div>

      <div v-else-if="orders.length === 0" class="bg-surface-dim border border-border rounded-2xl p-12 text-center">
        <Package :size="40" :stroke-width="1.5" class="mx-auto mb-4 text-text-tertiary" />
        <p class="text-lg font-medium mb-1 text-white">Aún no tienes pedidos</p>
        <p class="text-sm mb-6 text-text-secondary">Cuando realices tu primera compra, aparecerá aquí.</p>
        <router-link to="/#productos" class="btn-gold text-sm">
          Ir al catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col gap-4">
        <router-link
          v-for="order in orders"
          :key="order.id"
          :to="`/orders/${order.id}`"
          class="bg-surface-dim border border-border rounded-2xl p-5 block transition-colors hover:border-white/10"
        >
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <span class="text-base font-semibold text-white">Pedido #{{ order.id }}</span>
              <span class="block text-xs mt-0.5 text-text-secondary">{{ formatDate(order.created_at) }}</span>
            </div>
            <span :class="['badge', statusBadge[order.status]]">
              {{ orderStatusLabels[order.status] }}
            </span>
          </div>
          <div class="divider mb-3"></div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-sm text-text-secondary">
                {{ order.items.reduce((acc, i) => acc + i.quantity, 0) }} artículo(s)
              </span>
              <span
                v-if="order.coupon_code"
                class="badge badge-success text-[10px]"
              >
                {{ order.coupon_code }}
              </span>
            </div>
            <span class="text-lg font-semibold text-white">${{ formatPrice(order.total) }}</span>
          </div>

          <div
            v-if="order.invoice"
            class="flex flex-wrap items-center justify-between gap-2 mt-3 pt-3 border-t border-border-light"
          >
            <span class="inline-flex items-center gap-1.5 text-xs text-text-secondary">
              <FileText :size="13" :stroke-width="2" />
              Factura {{ order.invoice.bill_number }}
              <span v-if="order.invoice.status !== 'VALIDATED'" class="badge badge-warning text-[10px]">
                {{ order.invoice.status === 'PENDING' ? 'Pendiente DIAN' : 'Con error' }}
              </span>
            </span>
            <button
              v-if="order.invoice.status === 'VALIDATED' && order.invoice.bill_number"
              class="btn-ghost text-xs inline-flex items-center gap-1.5"
              :disabled="downloadingOrderId === order.id"
              @click.stop.prevent="downloadInvoicePdf(order)"
            >
              <Download :size="13" :stroke-width="2" />
              {{ downloadingOrderId === order.id ? 'Descargando...' : 'Descargar PDF' }}
            </button>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>
