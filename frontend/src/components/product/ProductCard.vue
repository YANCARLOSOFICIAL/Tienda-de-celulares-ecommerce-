<script setup lang="ts">
import { computed, ref } from 'vue'
import { ShoppingBag, Heart, MessageCircle, Scale } from '@lucide/vue'

import { formatPrice } from '@/api/products'
import { site, whatsappProductUrl } from '@/config/site'
import { wishlistApi } from '@/api/wishlist'
import { ApiError } from '@/api/client'
import type { Product } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useCompareStore } from '@/stores/compare'
import { useToast } from '@/composables/useToast'
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
const toast = useToast()
const adding = ref(false)
const added = ref(false)
const isWishlisted = ref(false)
const togglingWishlist = ref(false)

function goToDetail() {
  router.push({ name: 'product-detail', params: { id: props.product.id } })
}

const whatsappHref = computed(() => whatsappProductUrl(props.product.name, props.product.price))

const priceNumber = computed(() => Number(props.product.price))

const isInCompare = computed(() => compareStore.isInCompare(props.product.id))

async function addToCart() {
  if (!authStore.isAuthenticated) {
    toast.info('Inicia sesión para continuar')
    router.push({ name: 'login', query: { redirect: `/products/${props.product.id}` } })
    return
  }
  if (props.product.stock <= 0) return
  adding.value = true
  try {
    await cartStore.add(props.product.id, 1)
    added.value = true
    toast.success(`${props.product.name} se agregó al carrito`)
    setTimeout(() => (added.value = false), 2000)
  } catch (e) {
    added.value = false
    toast.error(e instanceof ApiError ? e.message : 'No se pudo agregar al carrito')
  } finally {
    adding.value = false
  }
}

async function toggleWishlist() {
  if (!authStore.isAuthenticated) {
    toast.info('Inicia sesión para continuar')
    router.push({ name: 'login', query: { redirect: `/products/${props.product.id}` } })
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
    toast.success(isWishlisted.value ? 'Agregado a favoritos' : 'Quitado de favoritos')
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'No se pudo actualizar favoritos')
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
    class="product-card flex flex-col overflow-hidden group"
    itemscope
    itemtype="https://schema.org/Product"
  >
    <div class="product-image cursor-pointer" @click="goToDetail">
      <img
        :src="product.image || 'https://placehold.co/400x400/f5f0e6/0a0906?text=Sin+imagen&font=inter'"
        :alt="product.name"
        loading="lazy"
        itemprop="image"
      />

      <button
        class="image-action top-3 right-3"
        :class="isWishlisted ? 'text-[#ef4444]' : 'text-text-secondary hover:text-[#ef4444]'"
        :disabled="togglingWishlist"
        @click.stop="toggleWishlist"
        :aria-label="isWishlisted ? 'Quitar de favoritos' : 'Agregar a favoritos'"
      >
        <Heart :size="16" :fill="isWishlisted ? 'currentColor' : 'none'" :stroke-width="1.75" />
      </button>

      <button
        class="image-action top-3 left-3"
        :class="isInCompare ? 'text-accent' : 'text-text-secondary hover:text-accent'"
        @click.stop="toggleCompare"
        :aria-label="isInCompare ? 'Quitar de comparar' : 'Agregar a comparar'"
      >
        <Scale :size="15" :stroke-width="1.75" />
      </button>

      <div
        v-if="product.stock <= 0"
        class="badge badge-danger absolute bottom-3 left-3 z-10"
      >
        Agotado
      </div>
    </div>

    <div class="product-content flex-1 flex flex-col">
      <span class="product-brand">{{ product.brand }}</span>
      <h3
        class="product-title cursor-pointer"
        itemprop="name"
        @click="goToDetail"
      >
        {{ product.name }}
      </h3>
      <p class="product-meta" itemprop="description">{{ product.model }}</p>

      <div class="mt-auto pt-4 space-y-3">
        <span class="product-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
          <span itemprop="price" :content="String(priceNumber)">${{ formatPrice(product.price) }}</span>
          <meta itemprop="priceCurrency" :content="site.currency" />
        </span>

        <div class="flex gap-2">
          <button
            v-if="product.stock > 0"
            class="btn-fill flex-1 text-[12px] py-3"
            :disabled="adding"
            @click="addToCart"
          >
            <ShoppingBag :size="15" :stroke-width="2" />
            {{ added ? 'Agregado' : adding ? 'Agregando...' : 'Agregar' }}
          </button>
          <a
            :href="whatsappHref"
            target="_blank"
            rel="noopener noreferrer"
            class="btn-outline px-4"
            aria-label="Consultar por WhatsApp"
            @click.stop
          >
            <MessageCircle :size="15" :stroke-width="2" />
          </a>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.product-card {
  background: var(--color-surface-dim);
  border: 1px solid var(--color-border);
  border-radius: 0;
  transition: border-color 0.35s ease, transform 0.4s ease;
}

.product-card:hover {
  border-color: rgba(240, 196, 25, 0.3);
  transform: translateY(-4px);
}

.product-image {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
  background: #12100a;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.image-action {
  position: absolute;
  z-index: 10;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 9, 6, 0.72);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(245, 240, 230, 0.16);
  border-radius: 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-action:hover {
  border-color: rgba(240, 196, 25, 0.5);
}

.product-content {
  padding: 20px;
}

.product-brand {
  font-family: var(--font-family-mono);
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-accent);
}

.product-title {
  font-family: var(--font-family-serif);
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.3;
  color: var(--color-text);
  margin-top: 8px;
  transition: color 0.3s ease;
}

.product-card:hover .product-title {
  color: var(--color-accent);
}

.product-meta {
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin-top: 4px;
}

.product-price {
  display: block;
  font-family: var(--font-family-serif);
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-accent);
}
</style>
