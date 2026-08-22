<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Heart, ShoppingBag, Trash2, ArrowLeft } from '@lucide/vue'

import { wishlistApi, type WishlistItem } from '../api/wishlist'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { formatPrice } from '../api/products'

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
  <section class="py-10 sm:py-16 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-8">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <Heart :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Mis favoritos</h1>
      </div>

      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="brutal-card p-5 flex gap-4">
          <div class="skeleton w-24 h-24 shrink-0"></div>
          <div class="flex-1 space-y-2">
            <div class="skeleton h-5 w-3/4"></div>
            <div class="skeleton h-4 w-1/2"></div>
          </div>
        </div>
      </div>

      <div v-else-if="items.length === 0" class="brutal-card p-12 text-center">
        <Heart :size="48" :stroke-width="1.5" class="mx-auto text-brutal-black/20 mb-4" />
        <p class="font-black text-2xl uppercase mb-2">Sin favoritos</p>
        <p class="text-brutal-black/60 mb-6">Aun no has agregado productos a tu lista de favoritos.</p>
        <router-link to="/shop" class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide">
          Ver tienda
        </router-link>
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="item in items"
          :key="item.id"
          class="brutal-card p-4 sm:p-5 flex flex-col sm:flex-row gap-4"
        >
          <router-link
            :to="{ name: 'product-detail', params: { id: item.product.id } }"
            class="shrink-0 w-24 h-24 bg-brutal-gray brutal-border overflow-hidden"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/111111/FFD60A?text=Sin+imagen&font=inter'"
              :alt="item.product.name"
              class="w-full h-full object-cover"
            />
          </router-link>

          <div class="flex-1 min-w-0">
            <router-link
              :to="{ name: 'product-detail', params: { id: item.product.id } }"
              class="font-black text-lg leading-tight hover:underline"
            >
              {{ item.product.name }}
            </router-link>
            <p class="text-sm text-brutal-black/50">{{ item.product.brand }}</p>
            <p class="font-black text-xl mt-1">${{ formatPrice(item.product.price) }}</p>
          </div>

          <div class="flex sm:flex-col gap-2 shrink-0">
            <button
              class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 flex items-center gap-2 text-sm uppercase tracking-wide disabled:opacity-60"
              :disabled="addingId === item.product.id || item.product.stock <= 0"
              @click="addToCart(item.product.id)"
            >
              <ShoppingBag :size="16" :stroke-width="2.5" />
              {{ item.product.stock <= 0 ? 'Agotado' : addingId === item.product.id ? 'Agregando...' : 'Carrito' }}
            </button>
            <button
              class="brutal-button bg-brutal-white text-red-600 px-4 py-2 flex items-center gap-2 text-sm uppercase tracking-wide"
              @click="removeItem(item.product.id)"
            >
              <Trash2 :size="16" :stroke-width="2.5" />
              Quitar
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
