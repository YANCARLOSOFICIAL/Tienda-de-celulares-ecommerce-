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
  <section class="page">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="page-header mb-10">
        <p class="eyebrow">Historial</p>
        <h1 class="page-title flex items-center gap-3">
          <Package :size="22" :stroke-width="1.75" class="text-accent" />
          Mis pedidos
        </h1>
      </div>

      <div v-if="loading" class="maison-panel p-12 text-center">
        <div class="skeleton h-5 w-48 mx-auto mb-3"></div>
        <div class="skeleton h-4 w-32 mx-auto"></div>
      </div>

      <div v-else-if="error" class="maison-panel p-12 text-center">
        <p class="text-sm text-text-secondary">{{ error }}</p>
        <button class="btn-outline mt-5" @click="loadOrders">Reintentar</button>
      </div>

      <div v-else-if="orders.length === 0" class="maison-panel p-16 text-center">
        <Package :size="40" :stroke-width="1.5" class="mx-auto mb-5 text-text-tertiary" />
        <p class="text-display text-xl mb-3">Aún no tienes pedidos</p>
        <p class="text-sm mb-8 text-text-secondary">Cuando realices tu primera compra, aparecerá aquí.</p>
        <router-link to="/shop" class="btn-fill">
          Ir al catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col gap-4">
        <router-link
          v-for="order in orders"
          :key="order.id"
          :to="`/orders/${order.id}`"
          class="maison-panel p-6 block transition-colors hover:border-[rgba(240,196,25,0.35)]"
        >
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <span class="text-base text-text" style="font-family: var(--font-family-serif);">Pedido #{{ order.id }}</span>
              <span class="block text-xs mt-1 text-text-tertiary">{{ formatDate(order.created_at) }}</span>
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
                class="badge badge-success"
              >
                {{ order.coupon_code }}
              </span>
            </div>
            <span class="text-lg font-semibold text-accent">${{ formatPrice(order.total) }}</span>
          </div>

          <div
            v-if="order.invoice"
            class="flex flex-wrap items-center justify-between gap-2 mt-3 pt-3 border-t border-border"
          >
            <span class="inline-flex items-center gap-1.5 text-xs text-text-secondary">
              <FileText :size="13" :stroke-width="2" />
              Factura {{ order.invoice.bill_number }}
              <span v-if="order.invoice.status !== 'VALIDATED'" class="badge badge-warning">
                {{ order.invoice.status === 'PENDING' ? 'Pendiente DIAN' : 'Con error' }}
              </span>
            </span>
            <button
              v-if="order.invoice.status === 'VALIDATED' && order.invoice.bill_number"
              class="btn-ghost text-xs"
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
