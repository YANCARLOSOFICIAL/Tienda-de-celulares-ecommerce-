<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Package, MapPin, Truck, XCircle } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { ordersApi, orderStatusLabels, type Order } from '../api/orders'
import { paymentsApi, paymentStatusLabel, type Payment } from '../api/payments'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const order = ref<Order | null>(null)
const payment = ref<Payment | null>(null)
const loading = ref(false)
const cancelling = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  await load()
})

async function load() {
  loading.value = true
  error.value = null
  try {
    order.value = await ordersApi.get(Number(route.params.id))
    try {
      payment.value = await paymentsApi.getByOrder(order.value.id)
    } catch {
      payment.value = null
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar el pedido.'
  } finally {
    loading.value = false
  }
}

async function cancelOrder() {
  if (!order.value || !confirm('Cancelar este pedido? El stock sera devuelto.')) return
  cancelling.value = true
  try {
    order.value = await ordersApi.cancel(order.value.id)
  } catch (e: any) {
    error.value = e.message || 'Error al cancelar el pedido'
  } finally {
    cancelling.value = false
  }
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
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
  <section class="py-16 sm:py-20 min-h-[70vh]" style="background: var(--color-surface-dim)">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-2xl sm:text-3xl font-semibold mb-1" style="color: var(--color-text)">Pedido #{{ route.params.id }}</h1>
        <router-link to="/orders" class="text-sm hover:underline" style="color: var(--color-accent)">
          ← Volver a mis pedidos
        </router-link>
      </div>

      <div v-if="loading" class="bento-card p-10 text-center">
        <div class="skeleton h-5 w-48 mx-auto mb-3"></div>
        <div class="skeleton h-4 w-32 mx-auto"></div>
      </div>

      <div v-else-if="error || !order" class="bento-card p-10 text-center">
        <p class="text-lg font-medium mb-1" style="color: var(--color-text)">Pedido no encontrado</p>
        <p class="text-sm" style="color: var(--color-text-secondary)">{{ error }}</p>
      </div>

        <div v-else class="flex flex-col gap-5 order-detail-glass">
        <div v-if="error" class="badge badge-danger w-full justify-center py-2 text-sm">
          {{ error }}
        </div>

        <div class="bento-card p-5">
          <div class="flex flex-wrap items-center gap-6 mb-4">
            <div>
              <span class="block text-xs mb-1" style="color: var(--color-text-secondary)">Fecha</span>
              <span class="text-sm font-medium" style="color: var(--color-text)">{{ formatDate(order.created_at) }}</span>
            </div>
            <div>
              <span class="block text-xs mb-1" style="color: var(--color-text-secondary)">Estado</span>
              <span :class="['badge', statusBadge[order.status]]">
                {{ orderStatusLabels[order.status] }}
              </span>
            </div>
            <div v-if="payment">
              <span class="block text-xs mb-1" style="color: var(--color-text-secondary)">Pago</span>
              <span class="badge badge-accent">
                {{ paymentStatusLabel[payment.status] || payment.status }}
              </span>
            </div>
          </div>
          <button
            v-if="order.status === 'PENDING' || order.status === 'CONFIRMED'"
            class="btn-danger text-sm"
            :disabled="cancelling"
            @click="cancelOrder"
          >
            <XCircle :size="16" :stroke-width="2" class="inline-block mr-1.5 align-[-3px]" />
            {{ cancelling ? 'Cancelando...' : 'Cancelar pedido' }}
          </button>
        </div>

        <div class="bento-card overflow-hidden">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="flex items-center gap-4 p-4"
            style="border-bottom: 1px solid var(--color-border-light)"
          >
            <div class="w-12 h-12 rounded-lg overflow-hidden shrink-0" style="background: var(--color-surface-dim)">
              <img
                v-if="item.product_image"
                :src="item.product_image"
                :alt="item.product_name"
                class="w-full h-full object-cover"
              />
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium truncate" style="color: var(--color-text)">{{ item.product_name }}</h3>
              <p class="text-xs" style="color: var(--color-text-secondary)">
                ${{ formatPrice(item.unit_price) }} × {{ item.quantity }}
              </p>
            </div>
            <span class="text-sm font-semibold whitespace-nowrap" style="color: var(--color-text)">${{ formatPrice(item.subtotal) }}</span>
          </div>
        </div>

        <div class="bento-card p-5 flex flex-col gap-2.5">
          <div class="flex justify-between text-sm" style="color: var(--color-text-secondary)">
            <span>Subtotal</span>
            <span style="color: var(--color-text)">${{ formatPrice(Number(order.total) + Number(order.discount_amount || 0)) }}</span>
          </div>
          <div v-if="order.shipping_cost != null" class="flex justify-between text-sm" style="color: var(--color-text-secondary)">
            <span>Envío</span>
            <span style="color: var(--color-text)">${{ formatPrice(order.shipping_cost) }}</span>
          </div>
          <div v-if="order.discount_amount && Number(order.discount_amount) > 0" class="flex justify-between text-sm font-medium" style="color: var(--color-success)">
            <span>Descuento ({{ order.coupon_code }})</span>
            <span>-${{ formatPrice(order.discount_amount) }}</span>
          </div>
          <div class="divider"></div>
          <div class="flex justify-between items-center">
            <span class="text-base font-medium" style="color: var(--color-text)">Total</span>
            <span class="text-xl font-semibold" style="color: var(--color-text)">${{ formatPrice(order.total) }}</span>
          </div>
        </div>

        <div v-if="order.shipping_address || order.address" class="bento-card p-5 flex items-start gap-3">
          <MapPin :size="18" :stroke-width="2" class="shrink-0 mt-0.5" style="color: var(--color-text-secondary)" />
          <div>
            <span class="block text-xs mb-1" style="color: var(--color-text-secondary)">Dirección de envío</span>
            <span class="text-sm" style="color: var(--color-text)">{{ order.shipping_address || order.address }}</span>
          </div>
        </div>

        <div v-if="order.shipping_method" class="bento-card p-5 flex items-start gap-3">
          <Truck :size="18" :stroke-width="2" class="shrink-0 mt-0.5" style="color: var(--color-text-secondary)" />
          <div>
            <span class="block text-xs mb-1" style="color: var(--color-text-secondary)">Método de envío</span>
            <span class="text-sm" style="color: var(--color-text)">{{ order.shipping_method }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.order-detail-glass > :deep(.bento-card) {
  border: 1px solid var(--color-border);
  background: rgba(10, 10, 10, 0.7);
  backdrop-filter: blur(12px);
  transition: border-color 0.3s, box-shadow 0.3s;
}
.order-detail-glass > :deep(.bento-card:hover) {
  border-color: var(--color-accent);
  box-shadow: 0 0 12px rgba(0, 212, 255, 0.1);
}
</style>
