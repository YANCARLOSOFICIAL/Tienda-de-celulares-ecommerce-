<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, X, ShoppingCart, Heart } from '@lucide/vue'
import { useCompareStore } from '@/stores/compare'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { formatPrice } from '@/api/products'

const router = useRouter()
const compareStore = useCompareStore()
const cartStore = useCartStore()
const authStore = useAuthStore()

const products = computed(() => compareStore.items)

const specCategories = computed(() => {
  const categories = [
    { label: 'Marca', key: 'brand' },
    { label: 'Modelo', key: 'model' },
    { label: 'Categoría', key: 'category' },
    { label: 'Precio', key: 'price' },
    { label: 'Stock', key: 'stock' },
  ]
  return categories
})

function getSpecValue(product: any, key: string): string {
  if (key === 'price') return `$${formatPrice(product.price)}`
  if (key === 'stock') return `${product.stock} disponibles`
  if (key === 'category') return product.category?.name || 'Sin categoría'
  return product[key] || '—'
}

function addToCart(productId: number) {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: '/compare' } })
    return
  }
  cartStore.add(productId, 1)
}
</script>

<template>
  <section class="page">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <button
        class="flex items-center gap-2 text-[12px] uppercase tracking-[0.14em] text-text-secondary hover:text-accent mb-8 transition-colors"
        @click="router.back()"
      >
        <ArrowLeft :size="15" :stroke-width="2" />
        Volver
      </button>

      <div class="page-header flex items-end justify-between gap-4">
        <div>
          <p class="eyebrow">Ficha comparativa</p>
          <h1 class="page-title">Comparar productos</h1>
        </div>
        <button
          class="btn-ghost"
          @click="compareStore.clear()"
        >
          Limpiar todo
        </button>
      </div>

      <div v-if="products.length === 0" class="maison-panel text-center py-20">
        <p class="text-display text-xl mb-5">No hay productos para comparar</p>
        <router-link to="/shop" class="btn-fill">
          Ir a la tienda
        </router-link>
      </div>

      <div v-else class="overflow-x-auto border border-border">
        <table class="maison-table min-w-[600px]">
          <thead>
            <tr>
              <th class="w-40"></th>
              <th
                v-for="product in products"
                :key="product.id"
                class="text-center"
              >
                <div class="relative inline-block">
                  <button
                    class="absolute -top-2 -right-2 p-1 bg-surface-dim border border-border text-text-tertiary hover:text-danger hover:border-danger transition-all z-10"
                    @click="compareStore.remove(product.id)"
                  >
                    <X :size="12" :stroke-width="2" />
                  </button>
                  <img
                    :src="product.image || 'https://placehold.co/200x200/f5f0e6/0a0906?text=IMG&font=inter'"
                    :alt="product.name"
                    class="w-32 h-32 object-cover mx-auto mb-3 border border-border"
                  />
                  <h3 class="text-sm font-serif font-semibold text-text mb-1">{{ product.name }}</h3>
                  <p class="text-xs text-text-secondary mb-3">{{ product.brand }}</p>
                  <div class="flex gap-2 justify-center">
                    <button
                      class="btn-fill text-xs px-3 py-2"
                      @click="addToCart(product.id)"
                    >
                      <ShoppingCart :size="12" :stroke-width="2" class="inline" />
                      Agregar
                    </button>
                  </div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="spec in specCategories"
              :key="spec.key"
            >
              <td class="text-sm font-medium text-text-tertiary uppercase tracking-wide text-[11px]">
                {{ spec.label }}
              </td>
              <td
                v-for="product in products"
                :key="product.id"
                class="p-4 text-center text-sm text-text"
              >
                {{ getSpecValue(product, spec.key) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>