<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, ShoppingBag, Trash2 } from '@lucide/vue'

import { wishlistApi, type WishlistItem } from '@/api/wishlist'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { formatPrice } from '@/api/products'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const items = ref<WishlistItem[]>([])
const loading = ref(true)
const addingId = ref<number | null>(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/wishlist' } })
    return
  }
  try {
    items.value = await wishlistApi.list()
  } catch {
    items.value = []
  } finally {
    loading.value = false
  }
})

async function addToCart(productId: number) {
  addingId.value = productId
  try {
    await cartStore.add(productId, 1)
  } catch { /* ignore */ } finally {
    addingId.value = null
  }
}

async function removeItem(productId: number) {
  try {
    await wishlistApi.remove(productId)
    items.value = items.value.filter((i) => i.product_id !== productId)
  } catch { /* ignore */ }
}
</script>

<template>
  <section class="page">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="page-header mb-10">
        <p class="eyebrow">Guardados</p>
        <h1 class="page-title flex items-center gap-3">
          <Heart :size="22" :stroke-width="1.75" class="text-accent" />
          Mis favoritos
        </h1>
      </div>

      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="maison-card p-4 flex flex-col gap-3">
          <div class="skeleton w-full aspect-square"></div>
          <div class="skeleton h-4 w-3/4"></div>
          <div class="skeleton h-3 w-1/2"></div>
          <div class="skeleton h-5 w-1/3"></div>
        </div>
      </div>

      <div v-else-if="items.length === 0" class="maison-panel p-16 text-center">
        <Heart :size="40" :stroke-width="1.5" class="mx-auto mb-5 text-text-tertiary" />
        <p class="text-display text-xl mb-3">Sin favoritos</p>
        <p class="text-sm mb-8 text-text-secondary">Aún no has agregado productos a tu lista de favoritos.</p>
        <router-link to="/shop" class="btn-fill">
          Ver tienda
        </router-link>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div
          v-for="item in items"
          :key="item.id"
          class="maison-card p-4 flex flex-col"
        >
          <router-link
            :to="{ name: 'product-detail', params: { id: item.product.id } }"
            class="block w-full aspect-square overflow-hidden mb-4 border border-border"
            style="background: var(--color-surface)"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/f5f0e6/0a0906?text=Sin+imagen&font=inter'"
              :alt="item.product.name"
              class="w-full h-full object-cover"
            />
          </router-link>

          <div class="flex-1 min-w-0 mb-4">
            <router-link
              :to="{ name: 'product-detail', params: { id: item.product.id } }"
              class="text-sm font-medium leading-tight block truncate text-text hover:text-accent transition-colors"
              style="font-family: var(--font-family-serif);"
            >
              {{ item.product.name }}
            </router-link>
            <p class="text-[10px] uppercase tracking-[0.16em] mt-1 text-text-tertiary">{{ item.product.brand }}</p>
            <p class="text-base font-medium mt-1.5 text-accent">${{ formatPrice(item.product.price) }}</p>
          </div>

          <div class="flex flex-col gap-2 mt-auto">
            <button
              class="btn-fill text-[11px] w-full"
              :disabled="addingId === item.product.id || item.product.stock <= 0"
              @click="addToCart(item.product.id)"
            >
              <ShoppingBag :size="14" :stroke-width="2" />
              {{ item.product.stock <= 0 ? 'Agotado' : addingId === item.product.id ? 'Agregando...' : 'Agregar al carrito' }}
            </button>
            <button
              class="btn-ghost text-[11px] w-full justify-center"
              style="color: var(--color-danger)"
              @click="removeItem(item.product.id)"
            >
              <Trash2 :size="14" :stroke-width="2" />
              Quitar
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
