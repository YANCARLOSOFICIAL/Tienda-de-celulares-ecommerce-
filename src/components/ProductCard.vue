<script setup lang="ts">
import { computed, ref } from 'vue'
import { ShoppingBag, Heart, MessageCircle, Scale } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { wishlistApi } from '../api/wishlist'
import type { Product } from '../stores/products'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { useCompareStore } from '../stores/compare'
import { useRouter } from 'vue-router'

const props = defineProps<{
  product: Product
}>()

const emit = defineEmits<{
  'add-to-cart': [product: Product]
  'toggle-wishlist': [productId: number]
}>()

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const compareStore = useCompareStore()
const adding = ref(false)
const added = ref(false)
const isWishlisted = ref(false)
const togglingWishlist = ref(false)

function goToDetail() {
  router.push({ name: 'product-detail', params: { id: props.product.id } })
}

const whatsappMessage = computed(() => {
  return encodeURIComponent(
    `¡Hola! Me interesa el ${props.product.name} por $${formatPrice(props.product.price)}. ¿Podrían darme más información?`
  )
})

const priceNumber = computed(() => Number(props.product.price))

const isInCompare = computed(() => compareStore.isInCompare(props.product.id))

async function addToCart() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: '/#productos' } })
    return
  }
  if (props.product.stock <= 0) return
  adding.value = true
  try {
    await cartStore.add(props.product.id, 1)
    added.value = true
    setTimeout(() => (added.value = false), 2000)
  } catch {
    added.value = false
  } finally {
    adding.value = false
  }
}

async function toggleWishlist() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: '/#productos' } })
    return
  }
  togglingWishlist.value = true
  try {
    if (isWishlisted.value) {
      await wishlistApi.remove(props.product.id)
    } else {
      await wishlistApi.add(props.product.id)
    }
    isWishlisted.value = !isWishlisted.value
    emit('toggle-wishlist', props.product.id)
  } catch {
    // silently fail
  } finally {
    togglingWishlist.value = false
  }
}

function toggleCompare() {
  compareStore.toggle(props.product)
}
</script>

<template>
  <article
    class="bento-card flex flex-col overflow-hidden group transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-accent/20"
    itemscope
    itemtype="https://schema.org/Product"
  >
    <div class="relative overflow-hidden rounded-xl aspect-square cursor-pointer bg-surface-dim" @click="goToDetail">
      <img
        :src="product.image || 'https://placehold.co/400x400/FAFAFA/86868B?text=Sin+imagen&font=inter'"
        :alt="product.name"
        loading="lazy"
        class="w-full h-full object-cover rounded-xl transition-all duration-500 group-hover:scale-105 group-hover:shadow-[0_0_20px_rgba(0,212,255,0.15)]"
        itemprop="image"
      />

      <button
        class="absolute top-3 right-3 w-9 h-9 flex items-center justify-center rounded-full bg-black/50 backdrop-blur-sm transition-all duration-200 hover:bg-black/70 hover:scale-110"
        :class="isWishlisted ? 'text-danger shadow-[0_0_12px_rgba(255,59,48,0.5)]' : 'text-text-secondary hover:text-danger'"
        :disabled="togglingWishlist"
        @click.stop="toggleWishlist"
        :aria-label="isWishlisted ? 'Quitar de favoritos' : 'Agregar a favoritos'"
      >
        <Heart :size="18" :fill="isWishlisted ? 'currentColor' : 'none'" :stroke-width="2" />
      </button>

      <button
        class="absolute top-3 left-3 w-9 h-9 flex items-center justify-center rounded-full bg-black/50 backdrop-blur-sm transition-all duration-200 hover:bg-black/70 hover:scale-110"
        :class="isInCompare ? 'text-accent shadow-[0_0_12px_rgba(0,212,255,0.5)]' : 'text-text-secondary hover:text-accent'"
        @click.stop="toggleCompare"
        :aria-label="isInCompare ? 'Quitar de comparar' : 'Agregar a comparar'"
      >
        <Scale :size="16" :stroke-width="2" />
      </button>

      <div
        v-if="product.stock <= 0"
        class="absolute top-3 left-3 bg-danger/90 text-white text-[11px] font-semibold px-3 py-1 rounded-full shadow-[0_0_10px_rgba(255,59,48,0.4)]"
      >
        Agotado
      </div>
    </div>

    <div class="flex-1 flex flex-col p-4">
      <p class="text-text-secondary text-sm mb-1" itemprop="brand">{{ product.brand }}</p>
      <h3
        class="font-semibold text-base leading-snug mb-2 line-clamp-2 cursor-pointer hover:text-accent transition-colors"
        itemprop="name"
        @click="goToDetail"
      >
        {{ product.name }}
      </h3>

      <div class="mt-auto pt-3 space-y-3">
        <span class="font-bold text-lg text-accent" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <span itemprop="price" :content="String(priceNumber)">${{ formatPrice(product.price) }}</span>
          <meta itemprop="priceCurrency" content="MXN" />
        </span>

        <div class="flex gap-2">
          <button
            v-if="product.stock > 0"
            class="btn-primary flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold hover:shadow-[0_0_20px_rgba(0,212,255,0.4)]"
            :disabled="adding"
            @click="addToCart"
          >
            <ShoppingBag :size="16" :stroke-width="2" />
            {{ added ? '¡Agregado!' : adding ? 'Agregando...' : 'Agregar' }}
          </button>
          <a
            :href="`https://wa.me/521234567890?text=${whatsappMessage}`"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-secondary flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl text-sm font-semibold hover:shadow-[0_0_15px_rgba(0,255,136,0.3)]"
            @click.stop
          >
            <MessageCircle :size="16" :stroke-width="2" />
          </a>
        </div>
      </div>
    </div>
  </article>
</template>
