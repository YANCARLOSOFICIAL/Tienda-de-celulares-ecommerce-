<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Package } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { ordersApi, orderStatusLabels, type Order } from '../api/orders'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

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
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <Package :size="20" :stroke-width="2" style="color: var(--color-text-secondary)" />
        <h1 class="text-2xl sm:text-3xl font-semibold" style="color: var(--color-text)">Mis pedidos</h1>
      </div>

      <div v-if="loading" class="bento-card p-10 text-center">
        <div class="skeleton h-5 w-48 mx-auto mb-3"></div>
        <div class="skeleton h-4 w-32 mx-auto"></div>
      </div>

      <div v-else-if="error" class="bento-card p-10 text-center">
        <p class="text-sm" style="color: var(--color-text-secondary)">{{ error }}</p>
        <button class="btn-secondary mt-4 text-sm" @click="loadOrders">Reintentar</button>
      </div>

      <div v-else-if="orders.length === 0" class="bento-card p-12 text-center">
        <Package :size="40" :stroke-width="1.5" class="mx-auto mb-4" style="color: var(--color-border)" />
        <p class="text-lg font-medium mb-1" style="color: var(--color-text)">Aún no tienes pedidos</p>
        <p class="text-sm mb-6" style="color: var(--color-text-secondary)">Cuando realices tu primera compra, aparecerá aquí.</p>
        <router-link to="/#productos" class="btn-primary text-sm">
          Ir al catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col gap-4">
        <router-link
          v-for="order in orders"
          :key="order.id"
          :to="`/orders/${order.id}`"
          class="bento-card p-5 block transition-colors order-card-neon"
        >
          <div class="flex flex-wrap items-center justify-between gap-3 mb-3">
            <div>
              <span class="text-base font-semibold" style="color: var(--color-text)">Pedido #{{ order.id }}</span>
              <span class="block text-xs mt-0.5" style="color: var(--color-text-secondary)">{{ formatDate(order.created_at) }}</span>
            </div>
            <span :class="['badge', statusBadge[order.status]]">
              {{ orderStatusLabels[order.status] }}
            </span>
          </div>
          <div class="divider mb-3"></div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-sm" style="color: var(--color-text-secondary)">
                {{ order.items.reduce((acc, i) => acc + i.quantity, 0) }} artículo(s)
              </span>
              <span
                v-if="order.coupon_code"
                class="badge badge-success text-[10px]"
              >
                {{ order.coupon_code }}
              </span>
            </div>
            <span class="text-lg font-semibold" style="color: var(--color-text)">${{ formatPrice(order.total) }}</span>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.order-card-neon {
  border: 1px solid var(--color-border);
  transition: border-color 0.3s, box-shadow 0.3s;
}
.order-card-neon:hover {
  border-color: var(--color-accent);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.12);
}
</style>
