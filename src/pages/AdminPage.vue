<script setup lang="ts">
import { ref } from 'vue'
import { ChartNoAxesCombined, FolderKanban, PackageOpen } from '@lucide/vue'

import AdminCategories from '../components/admin/AdminCategories.vue'
import AdminOrders from '../components/admin/AdminOrders.vue'
import AdminProducts from '../components/admin/AdminProducts.vue'
import AdminCoupons from '../components/admin/AdminCoupons.vue'
import AdminDashboard from './AdminDashboard.vue'

type Tab = 'dashboard' | 'products' | 'categories' | 'orders' | 'coupons'

const tabs: { id: Tab; label: string; icon: typeof ChartNoAxesCombined }[] = [
  { id: 'dashboard', label: 'Dashboard', icon: ChartNoAxesCombined },
  { id: 'products', label: 'Productos', icon: ChartNoAxesCombined },
  { id: 'categories', label: 'Categorías', icon: FolderKanban },
  { id: 'orders', label: 'Pedidos', icon: PackageOpen },
  { id: 'coupons', label: 'Cupones', icon: ChartNoAxesCombined },
]

const activeTab = ref<Tab>('dashboard')
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="brutal-card p-8 mb-8">
      <h1 class="font-black text-3xl lg:text-4xl uppercase brutal-shadow-sm inline-block">
        Panel de administración
      </h1>
      <p class="text-brutal-black/60 mt-2 font-semibold">Gestiona el catálogo, las categorías y los pedidos de Tienda Cell.</p>
    </div>

    <div class="flex flex-wrap gap-2 mb-8">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="flex items-center gap-2 brutal-border px-4 py-3 font-black uppercase text-sm transition-all"
        :class="activeTab === tab.id ? 'bg-brutal-yellow brutal-shadow-sm' : 'bg-brutal-white hover:bg-brutal-gray/50'"
        @click="activeTab = tab.id"
      >
        <component :is="tab.icon" :size="18" :stroke-width="2.5" />
        {{ tab.label }}
      </button>
    </div>

    <AdminDashboard v-if="activeTab === 'dashboard'" />
    <AdminProducts v-else-if="activeTab === 'products'" />
    <AdminCategories v-else-if="activeTab === 'categories'" />
    <AdminOrders v-else-if="activeTab === 'orders'" />
    <AdminCoupons v-else />
  </div>
</template>