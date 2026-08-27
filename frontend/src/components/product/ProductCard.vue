<script setup lang="ts">
import { computed, ref } from 'vue'
import { ShoppingBag, Heart, MessageCircle, Scale } from '@lucide/vue'

import { formatPrice } from '@/api/products'
import { wishlistApi } from '@/api/wishlist'
import type { Product } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useCompareStore } from '@/stores/compare'
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
    class="premium-card flex flex-col overflow-hidden group"
    itemscope
    itemtype="https://schema.org/Product"
  >
    <div class="premium-image cursor-pointer" @click="goToDetail">
      <img
        :src="product.image || 'https://placehold.co/400x400/FAFAFA/86868B?text=Sin+imagen&font=inter'"
        :alt="product.name"
        loading="lazy"
        itemprop="image"
      />

      <button
        class="absolute top-3 right-3 w-9 h-9 flex items-center justify-center rounded-full glass transition-all duration-300 hover:scale-110 z-10"
        :class="isWishlisted ? 'text-red-400' : 'text-text-secondary hover:text-red-400'"
        :disabled="togglingWishlist"
        @click.stop="toggleWishlist"
        :aria-label="isWishlisted ? 'Quitar de favoritos' : 'Agregar a favoritos'"
      >
        <Heart :size="18" :fill="isWishlisted ? 'currentColor' : 'none'" :stroke-width="2" />
      </button>

      <button
        class="absolute top-3 left-3 w-9 h-9 flex items-center justify-center rounded-full glass transition-all duration-300 hover:scale-110 z-10"
        :class="isInCompare ? 'text-accent' : 'text-text-secondary hover:text-accent'"
        @click.stop="toggleCompare"
        :aria-label="isInCompare ? 'Quitar de comparar' : 'Agregar a comparar'"
      >
        <Scale :size="16" :stroke-width="2" />
      </button>

      <div
        v-if="product.stock <= 0"
        class="absolute top-3 left-3 badge badge-danger z-10"
      >
        Agotado
      </div>
    </div>

    <div class="premium-content flex-1 flex flex-col">
      <span class="category-badge mb-2">{{ product.brand }}</span>
      <div class="premium-header">
        <h3
          class="premium-title cursor-pointer hover:text-gold-light transition-colors duration-300"
          itemprop="name"
          @click="goToDetail"
        >
          {{ product.name }}
        </h3>
      </div>
      <p class="premium-description" itemprop="description">{{ product.brand }} {{ product.model }}</p>

      <div class="mt-auto pt-2 space-y-3">
        <span class="text-gold font-bold text-xl" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <span itemprop="price" :content="String(priceNumber)">${{ formatPrice(product.price) }}</span>
          <meta itemprop="priceCurrency" content="MXN" />
        </span>

        <div class="flex gap-2">
          <button
            v-if="product.stock > 0"
            class="btn-gold flex-1 flex items-center justify-center gap-2 py-2.5 rounded-full text-sm font-semibold"
            :disabled="adding"
            @click="addToCart"
          >
            <ShoppingBag :size="16" :stroke-width="2" />
            {{ added ? 'Agregado!' : adding ? 'Agregando...' : 'Agregar' }}
          </button>
          <a
            :href="`https://wa.me/521234567890?text=${whatsappMessage}`"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-secondary flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-full text-sm font-semibold"
            @click.stop
          >
            <MessageCircle :size="16" :stroke-width="2" />
          </a>
        </div>
      </div>
    </div>
  </article>
</template>
