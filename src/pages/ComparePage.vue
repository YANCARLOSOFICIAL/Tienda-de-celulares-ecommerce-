<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, X, ShoppingCart, Heart } from '@lucide/vue'
import { useCompareStore } from '../stores/compare'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { formatPrice } from '../api/products'

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
  <section class="py-10 sm:py-16 bg-surface min-h-[70vh]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <button
        class="flex items-center gap-2 text-sm text-text-secondary hover:text-text mb-8 transition-colors"
        @click="router.back()"
      >
        <ArrowLeft :size="16" :stroke-width="2" />
        Volver
      </button>

      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-text" style="font-family: var(--font-family-serif);">
          Comparar productos
        </h1>
        <button
          class="btn-ghost text-sm"
          @click="compareStore.clear()"
        >
          Limpiar todo
        </button>
      </div>

      <div v-if="products.length === 0" class="text-center py-20">
        <p class="text-text-secondary text-lg mb-4">No hay productos para comparar</p>
        <router-link to="/shop" class="btn-gold px-6 py-3 inline-block text-sm">
          Ir a la tienda
        </router-link>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full min-w-[600px]">
          <thead>
            <tr>
              <th class="w-40 p-4"></th>
              <th
                v-for="product in products"
                :key="product.id"
                class="p-4 text-center"
              >
                <div class="relative inline-block">
                  <button
                    class="absolute -top-2 -right-2 p-1 bg-surface-dim border border-border rounded-full text-text-tertiary hover:text-danger hover:border-danger transition-all z-10"
                    @click="compareStore.remove(product.id)"
                  >
                    <X :size="12" :stroke-width="2" />
                  </button>
                  <img
                    :src="product.image || 'https://placehold.co/200x200/1C1C1E/8E8E93?text=IMG&font=inter'"
                    :alt="product.name"
                    class="w-32 h-32 object-cover rounded-2xl mx-auto mb-3 border border-border"
                  />
                  <h3 class="text-sm font-semibold text-text mb-1">{{ product.name }}</h3>
                  <p class="text-xs text-text-secondary mb-3">{{ product.brand }}</p>
                  <div class="flex gap-2 justify-center">
                    <button
                      class="btn-gold text-xs px-3 py-1.5"
                      @click="addToCart(product.id)"
                    >
                      <ShoppingCart :size="12" :stroke-width="2" class="inline mr-1" />
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
              class="border-t border-border"
            >
              <td class="p-4 text-sm font-medium text-text-secondary">
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