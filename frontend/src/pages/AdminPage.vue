<script setup lang="ts">
import { ref } from 'vue'
import {
  LayoutDashboard,
  Package,
  FolderKanban,
  ClipboardList,
  Ticket,
} from '@lucide/vue'

import AdminCategories from '@/components/admin/AdminCategories.vue'
import AdminOrders from '@/components/admin/AdminOrders.vue'
import AdminProducts from '@/components/admin/AdminProducts.vue'
import AdminCoupons from '@/components/admin/AdminCoupons.vue'
import AdminDashboard from './AdminDashboard.vue'

type Tab = 'dashboard' | 'products' | 'categories' | 'orders' | 'coupons'

const tabs: { id: Tab; label: string; icon: typeof LayoutDashboard }[] = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'products', label: 'Productos', icon: Package },
  { id: 'categories', label: 'Categorías', icon: FolderKanban },
  { id: 'orders', label: 'Pedidos', icon: ClipboardList },
  { id: 'coupons', label: 'Cupones', icon: Ticket },
]

const activeTab = ref<Tab>('dashboard')
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-text" style="font-family: var(--font-family-serif);">Panel de administración</h1>
      <p class="text-secondary mt-1">Gestiona el catálogo, las categorías y los pedidos de Tienda Cell.</p>
    </div>

    <nav class="flex flex-wrap gap-2 mb-8 bg-surface-dim border border-border rounded-2xl p-2">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
        :class="
          activeTab === tab.id
            ? 'bg-gold/15 text-gold border-b-2 border-gold'
            : 'text-text-tertiary hover:bg-white/5 hover:text-white'
        "
        @click="activeTab = tab.id"
      >
        <component :is="tab.icon" :size="16" :stroke-width="2" />
        {{ tab.label }}
      </button>
    </nav>

    <AdminDashboard v-if="activeTab === 'dashboard'" />
    <AdminProducts v-else-if="activeTab === 'products'" />
    <AdminCategories v-else-if="activeTab === 'categories'" />
    <AdminOrders v-else-if="activeTab === 'orders'" />
    <AdminCoupons v-else />
  </div>
</template>
