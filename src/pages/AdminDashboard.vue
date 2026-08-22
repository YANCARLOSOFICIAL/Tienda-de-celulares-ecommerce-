<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ShoppingCart, DollarSign, Package, Users, TrendingUp } from '@lucide/vue'

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

const summaryCards = ref<{ label: string; value: string; icon: typeof Package; color: string; bgColor: string }[]>([])

watch(stats, (s) => {
  if (!s) return
  summaryCards.value = [
    { label: 'Pedidos', value: String(s.total_orders), icon: ShoppingCart, color: 'text-gold', bgColor: 'bg-gold/10' },
    { label: 'Ingresos', value: '$' + formatPrice(s.total_revenue), icon: DollarSign, color: 'text-accent', bgColor: 'bg-accent/10' },
    { label: 'Productos', value: String(s.total_products), icon: Package, color: 'text-gold', bgColor: 'bg-gold/10' },
    { label: 'Usuarios', value: String(s.total_users), icon: Users, color: 'text-silver', bgColor: 'bg-silver/10' },
  ]
})

const statusColorMap: Record<string, string> = {
  pending: 'bg-gold',
  confirmed: 'bg-accent',
  shipped: 'bg-silver',
  delivered: 'bg-accent',
  cancelled: 'bg-danger',
}

const statusBadgeMap: Record<string, string> = {
  pending: 'badge-warning',
  confirmed: 'badge-accent',
  shipped: 'badge-accent',
  delivered: 'badge-success',
  cancelled: 'badge-danger',
}
</script>

<template>
  <div class="bento-grid">
    <!-- Loading skeletons -->
    <template v-if="loading">
      <div v-for="i in 4" :key="i" class="bento-card-static">
        <div class="skeleton h-4 w-24 mb-3"></div>
        <div class="skeleton h-8 w-32"></div>
      </div>
    </template>

    <template v-else-if="stats">
      <!-- Summary cards -->
      <div
        v-for="card in summaryCards"
        :key="card.label"
        class="bento-card-static"
      >
        <div class="flex items-center gap-3 mb-3">
          <span :class="[card.bgColor, 'w-10 h-10 rounded-full flex items-center justify-center']">
            <component :is="card.icon" :size="18" :stroke-width="2" :class="card.color" />
          </span>
          <span class="text-secondary text-xs uppercase tracking-wider font-medium">{{ card.label }}</span>
        </div>
        <p class="text-3xl font-bold text-text">{{ card.value }}</p>
      </div>

      <!-- Orders by status -->
      <div class="bento-card bento-span-2 glass">
        <div class="flex items-center gap-2 mb-4">
          <TrendingUp :size="18" :stroke-width="2" class="text-text-tertiary" />
          <h3 class="font-semibold text-text">Pedidos por estado</h3>
        </div>
        <div class="space-y-3">
          <div
            v-for="(count, status) in stats.orders_by_status"
            :key="status"
            class="flex items-center gap-3"
          >
            <span class="text-sm text-secondary w-28 shrink-0">
              {{ orderStatusLabels[status as OrderStatus] || status }}
            </span>
            <div class="flex-1 h-2 bg-surface-dim rounded-full overflow-hidden">
              <div
                :class="[statusColorMap[status] || 'bg-gold']"
                class="h-full rounded-full transition-all duration-500"
                :style="{ width: stats.total_orders ? `${(count / stats.total_orders) * 100}%` : '0%' }"
              ></div>
            </div>
            <span class="text-sm font-semibold text-text w-8 text-right">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- Top products -->
      <div class="bento-card-static">
        <div class="flex items-center gap-2 mb-4">
          <Package :size="18" :stroke-width="2" class="text-text-tertiary" />
          <h3 class="font-semibold text-text">Productos más vendidos</h3>
        </div>
        <div v-if="stats.top_products.length === 0" class="text-secondary text-sm">
          Sin ventas aún
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="(product, index) in stats.top_products.slice(0, 5)"
            :key="index"
            class="flex items-center gap-3 py-2 border-b border-border-light last:border-b-0"
          >
            <span class="text-xs font-bold text-secondary w-5 text-center">{{ index + 1 }}</span>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium text-text truncate">{{ product.name }}</p>
              <p class="text-xs text-secondary">{{ product.total_sold }} vendidos</p>
            </div>
            <span class="text-sm font-semibold text-text shrink-0">${{ formatPrice(product.total_revenue) }}</span>
          </div>
        </div>
      </div>

      <!-- Recent orders -->
      <div class="bento-card bento-span-2 glass">
        <div class="flex items-center gap-2 mb-4">
          <ShoppingCart :size="18" :stroke-width="2" class="text-text-tertiary" />
          <h3 class="font-semibold text-text">Pedidos recientes</h3>
        </div>
        <div v-if="stats.recent_orders.length === 0" class="text-secondary text-sm">
          Sin pedidos aún
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-border">
                <th class="text-left py-2 text-xs font-medium text-secondary uppercase tracking-wider">#</th>
                <th class="text-left py-2 text-xs font-medium text-secondary uppercase tracking-wider">Estado</th>
                <th class="text-left py-2 text-xs font-medium text-secondary uppercase tracking-wider">Total</th>
                <th class="text-left py-2 text-xs font-medium text-secondary uppercase tracking-wider">Fecha</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="order in stats.recent_orders"
                :key="order.id"
                class="border-b border-border-light hover:bg-accent/5 transition-colors duration-100"
              >
                <td class="py-3 font-medium text-text">#{{ order.id }}</td>
                <td class="py-3">
                  <span :class="['badge text-xs', statusBadgeMap[order.status] || 'badge']">
                    {{ orderStatusLabels[order.status as OrderStatus] || order.status }}
                  </span>
                </td>
                <td class="py-3 font-semibold text-text">${{ formatPrice(order.total) }}</td>
                <td class="py-3 text-secondary">{{ new Date(order.created_at).toLocaleDateString('es-MX') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>
