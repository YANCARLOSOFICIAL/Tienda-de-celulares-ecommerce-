<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Package } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { ordersApi, orderStatusLabels, type Order } from '../api/orders'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const order = ref<Order | null>(null)
const loading = ref(false)
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
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar el pedido.'
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
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <Package :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <div>
          <h1 class="font-black text-3xl uppercase">Pedido #{{ route.params.id }}</h1>
          <router-link to="/orders" class="text-sm font-bold underline text-brutal-black/70">
            ← Volver a mis pedidos
          </router-link>
        </div>
      </div>

      <div v-if="loading" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg">Cargando pedido...</p>
      </div>

      <div v-else-if="error || !order" class="brutal-card p-10 text-center">
        <p class="font-black text-xl uppercase mb-2">Pedido no encontrado</p>
        <p class="text-brutal-black/60">{{ error }}</p>
      </div>

      <div v-else class="space-y-6">
        <div class="brutal-card p-6">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <span class="block text-sm text-brutal-black/60">Fecha</span>
              <span class="font-bold">{{ formatDate(order.created_at) }}</span>
            </div>
            <div>
              <span class="block text-sm text-brutal-black/60">Estado</span>
              <span :class="['font-black text-xs uppercase px-3 py-1 brutal-border inline-block mt-1', statusClasses[order.status]]">
                {{ orderStatusLabels[order.status] }}
              </span>
            </div>
          </div>
        </div>

        <div class="brutal-card overflow-hidden">
          <div
            v-for="item in order.items"
            :key="item.id"
            class="flex items-center justify-between gap-4 p-5 border-b-4 border-brutal-black last:border-b-0"
          >
            <div class="min-w-0">
              <h3 class="font-black leading-tight">{{ item.product_name }}</h3>
              <p class="text-sm text-brutal-black/60">
                ${{ formatPrice(item.unit_price) }} × {{ item.quantity }}
              </p>
            </div>
            <span class="font-black whitespace-nowrap">${{ formatPrice(item.subtotal) }}</span>
          </div>
        </div>

        <div class="brutal-card p-6 flex justify-between items-center">
          <span class="font-black text-xl uppercase">Total</span>
          <span class="font-black text-2xl">${{ formatPrice(order.total) }}</span>
        </div>
      </div>
    </div>
  </section>
</template>
