<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Package, ShoppingCart, DollarSign, Users, TrendingUp } from '@lucide/vue'

import { adminApi, type AdminStats } from '../api/admin'
import { formatPrice } from '../api/products'
import { orderStatusLabels, type OrderStatus } from '../api/orders'

const stats = ref<AdminStats | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    stats.value = await adminApi.getStats()
  } catch {
    stats.value = null
  } finally {
    loading.value = false
  }
})

const summaryCards = ref<{ label: string; value: string; icon: typeof Package; color: string }[]>([])

import { watch } from 'vue'
watch(stats, (s) => {
  if (!s) return
  summaryCards.value = [
    { label: 'Pedidos', value: String(s.total_orders), icon: ShoppingCart, color: 'bg-brutal-yellow' },
    { label: 'Ingresos', value: '$' + formatPrice(s.total_revenue), icon: DollarSign, color: 'bg-green-200' },
    { label: 'Productos', value: String(s.total_products), icon: Package, color: 'bg-blue-200' },
    { label: 'Usuarios', value: String(s.total_users), icon: Users, color: 'bg-purple-200' },
  ]
})
</script>

<template>
  <div class="space-y-8">
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="brutal-card p-6">
        <div class="skeleton h-4 w-24 mb-3"></div>
        <div class="skeleton h-8 w-32"></div>
      </div>
    </div>

    <template v-else-if="stats">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="card in summaryCards" :key="card.label" class="brutal-card p-5">
          <div class="flex items-center gap-3 mb-3">
            <span :class="[card.color, 'p-2 brutal-border']">
              <component :is="card.icon" :size="18" :stroke-width="2.5" />
            </span>
            <span class="text-sm font-bold uppercase text-brutal-black/60">{{ card.label }}</span>
          </div>
          <p class="font-black text-2xl lg:text-3xl">{{ card.value }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="brutal-card p-5">
          <h3 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
            <TrendingUp :size="18" :stroke-width="2.5" />
            Pedidos por estado
          </h3>
          <div class="space-y-3">
            <div v-for="(count, status) in stats.orders_by_status" :key="status" class="flex items-center justify-between">
              <span class="text-sm font-semibold">{{ orderStatusLabels[status as OrderStatus] || status }}</span>
              <div class="flex items-center gap-3">
                <div class="w-32 h-3 brutal-border bg-brutal-gray overflow-hidden">
                  <div
                    class="h-full bg-brutal-yellow transition-all"
                    :style="{ width: stats.total_orders ? `${(count / stats.total_orders) * 100}%` : '0%' }"
                  ></div>
                </div>
                <span class="font-black text-sm w-8 text-right">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="brutal-card p-5">
          <h3 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
            <Package :size="18" :stroke-width="2.5" />
            Productos mas vendidos
          </h3>
          <div v-if="stats.top_products.length === 0" class="text-brutal-black/40 text-sm font-semibold">
            Sin ventas aun
          </div>
          <div v-else class="space-y-3">
            <div v-for="(product, index) in stats.top_products" :key="index" class="flex items-center justify-between py-2 border-b-2 border-brutal-black/10 last:border-b-0">
              <div class="min-w-0">
                <p class="font-bold text-sm truncate">{{ product.name }}</p>
                <p class="text-xs text-brutal-black/50">{{ product.total_sold }} vendidos</p>
              </div>
              <span class="font-black text-sm">${{ formatPrice(product.total_revenue) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="brutal-card p-5">
        <h3 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
          <ShoppingCart :size="18" :stroke-width="2.5" />
          Pedidos recientes
        </h3>
        <div v-if="stats.recent_orders.length === 0" class="text-brutal-black/40 text-sm font-semibold">
          Sin pedidos aun
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b-4 border-brutal-black">
                <th class="text-left py-2 font-black uppercase">#</th>
                <th class="text-left py-2 font-black uppercase">Estado</th>
                <th class="text-left py-2 font-black uppercase">Total</th>
                <th class="text-left py-2 font-black uppercase">Fecha</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in stats.recent_orders" :key="order.id" class="border-b-2 border-brutal-black/10">
                <td class="py-2 font-bold">#{{ order.id }}</td>
                <td class="py-2">
                  <span class="font-bold text-xs uppercase bg-brutal-yellow px-2 py-1 brutal-border">
                    {{ orderStatusLabels[order.status as OrderStatus] || order.status }}
                  </span>
                </td>
                <td class="py-2 font-black">${{ formatPrice(order.total) }}</td>
                <td class="py-2 text-brutal-black/60">{{ new Date(order.created_at).toLocaleDateString('es-MX') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>
