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

const statusClasses: Record<string, string> = {
  PENDING: 'bg-brutal-yellow text-brutal-black',
  CONFIRMED: 'bg-blue-100 text-blue-800',
  PROCESSING: 'bg-purple-100 text-purple-800',
  SHIPPED: 'bg-orange-100 text-orange-800',
  DELIVERED: 'bg-green-100 text-green-800',
  CANCELLED: 'bg-red-100 text-red-700',
}
</script>

<template>
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <Package :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Mis pedidos</h1>
      </div>

      <div v-if="loading" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg">Cargando pedidos...</p>
      </div>

      <div v-else-if="error" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg text-brutal-black">{{ error }}</p>
        <button class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 mt-4" @click="loadOrders">
          Reintentar
        </button>
      </div>

      <div v-else-if="orders.length === 0" class="brutal-card p-10 text-center">
        <p class="font-black text-2xl uppercase mb-4">Aún no tienes pedidos</p>
        <p class="text-brutal-black/60 mb-6">Cuando realices tu primera compra, aparecerá aquí.</p>
        <router-link to="/#productos" class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide">
          Ir al catálogo
        </router-link>
      </div>

      <div v-else class="space-y-6">
        <router-link
          v-for="order in orders"
          :key="order.id"
          :to="`/orders/${order.id}`"
          class="brutal-card p-6 block hover:-translate-y-0.5 transition-transform"
        >
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div>
              <span class="font-black text-xl">Pedido #{{ order.id }}</span>
              <span class="block text-sm text-brutal-black/60">{{ formatDate(order.created_at) }}</span>
            </div>
            <span :class="['font-black text-xs uppercase px-3 py-1 brutal-border', statusClasses[order.status]]">
              {{ orderStatusLabels[order.status] }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm text-brutal-black/70">
              {{ order.items.reduce((acc, i) => acc + i.quantity, 0) }} artículo(s)
            </span>
            <span class="font-black text-xl">${{ formatPrice(order.total) }}</span>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>
