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
  <section class="py-16 sm:py-20 min-h-[70vh]" style="background: var(--color-surface-dim)">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <Heart :size="20" :stroke-width="2" style="color: var(--color-text-secondary)" />
        <h1 class="text-2xl sm:text-3xl font-semibold" style="font-family: var(--font-family-serif); color: var(--color-text)">Mis favoritos</h1>
      </div>

      <div v-if="loading" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="bento-card p-4 flex flex-col gap-3">
          <div class="skeleton w-full aspect-square rounded-lg"></div>
          <div class="skeleton h-4 w-3/4"></div>
          <div class="skeleton h-3 w-1/2"></div>
          <div class="skeleton h-5 w-1/3"></div>
        </div>
      </div>

      <div v-else-if="items.length === 0" class="bento-card p-12 text-center">
        <Heart :size="40" :stroke-width="1.5" class="mx-auto mb-4" style="color: var(--color-border)" />
        <p class="text-lg font-medium mb-1" style="color: var(--color-text)">Sin favoritos</p>
        <p class="text-sm mb-6" style="color: var(--color-text-secondary)">Aún no has agregado productos a tu lista de favoritos.</p>
        <router-link to="/shop" class="btn-gold text-sm">
          Ver tienda
        </router-link>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <div
          v-for="item in items"
          :key="item.id"
          class="bento-card p-4 flex flex-col wishlist-card-neon"
        >
          <router-link
            :to="{ name: 'product-detail', params: { id: item.product.id } }"
            class="block w-full aspect-square rounded-lg overflow-hidden mb-3"
            style="background: var(--color-surface-dim)"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/FAFAFA/E5E5EA?text=Sin+imagen&font=inter'"
              :alt="item.product.name"
              class="w-full h-full object-cover"
            />
          </router-link>

          <div class="flex-1 min-w-0 mb-3">
            <router-link
              :to="{ name: 'product-detail', params: { id: item.product.id } }"
              class="text-sm font-medium leading-tight hover:underline block truncate"
              style="color: var(--color-text)"
            >
              {{ item.product.name }}
            </router-link>
            <p class="text-xs mt-0.5" style="color: var(--color-text-secondary)">{{ item.product.brand }}</p>
            <p class="text-base font-semibold mt-1" style="color: var(--color-text)">${{ formatPrice(item.product.price) }}</p>
          </div>

          <div class="flex flex-col gap-2 mt-auto">
            <button
              class="btn-gold text-xs w-full"
              :disabled="addingId === item.product.id || item.product.stock <= 0"
              @click="addToCart(item.product.id)"
            >
              <ShoppingBag :size="14" :stroke-width="2" class="inline-block mr-1 align-[-2px]" />
              {{ item.product.stock <= 0 ? 'Agotado' : addingId === item.product.id ? 'Agregando...' : 'Agregar al carrito' }}
            </button>
            <button
              class="btn-ghost text-xs w-full"
              style="color: var(--color-danger)"
              @click="removeItem(item.product.id)"
            >
              <Trash2 :size="14" :stroke-width="2" class="inline-block mr-1 align-[-2px]" />
              Quitar
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.wishlist-card-neon {
  border: 1px solid var(--color-border);
  transition: border-color 0.3s, box-shadow 0.3s;
}
.wishlist-card-neon:hover {
  border-color: var(--color-accent);
  box-shadow: 0 0 15px rgba(212, 169, 74, 0.15);
}
</style>
