<script setup lang="ts">
import { computed, ref } from 'vue'
import { ShoppingBag } from '@lucide/vue'

import { formatPrice } from '../api/products'
import type { Product } from '../stores/products'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps<{
  product: Product
  visible: boolean
  index: number
}>()

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const adding = ref(false)
const added = ref(false)

function goToDetail() {
  router.push({ name: 'product-detail', params: { id: props.product.id } })
}

const whatsappMessage = computed(() => {
  return encodeURIComponent(
    `¡Hola! Me interesa el ${props.product.name} por $${formatPrice(props.product.price)}. ¿Podrían darme más información?`
  )
})

const priceNumber = computed(() => Number(props.product.price))

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
</script>

<template>
  <article
    :class="[
      'brutal-card flex flex-col overflow-hidden group',
      'animate-fade-in-up',
      visible ? 'visible' : ''
    ]"
    :style="{ transitionDelay: `${index * 100}ms` }"
    itemscope
    itemtype="https://schema.org/Product"
  >
    <div class="relative overflow-hidden bg-brutal-gray aspect-square cursor-pointer" @click="goToDetail">
      <img
        :src="product.image || 'https://placehold.co/400x400/111111/FFD60A?text=Sin+imagen&font=inter'"
        :alt="product.name"
        loading="lazy"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        itemprop="image"
      />
      <div class="absolute top-2 right-2 bg-brutal-black text-brutal-white text-[10px] font-bold px-2 py-1 uppercase brutal-border">
        {{ product.brand }}
      </div>
      <div
        v-if="product.stock <= 0"
        class="absolute top-2 left-2 bg-brutal-black text-brutal-white font-black text-sm px-3 py-1 brutal-border brutal-shadow-sm uppercase"
      >
        Agotado
      </div>
    </div>

    <div class="flex-1 flex flex-col p-4 sm:p-5">
      <h3
        class="font-black text-lg sm:text-xl leading-tight mb-1 cursor-pointer hover:underline"
        itemprop="name"
        @click="goToDetail"
      >
        {{ product.name }}
      </h3>
      <p class="text-sm text-brutal-black/60 mb-3 line-clamp-2" itemprop="description">{{ product.description }}</p>

      <div class="mt-auto space-y-3">
        <div class="flex items-baseline gap-2">
          <span class="font-black text-2xl sm:text-3xl text-brutal-black" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
            <span itemprop="price" :content="String(priceNumber)">${{ formatPrice(product.price) }}</span>
            <meta itemprop="priceCurrency" content="MXN" />
          </span>
        </div>

        <div class="flex flex-col gap-2">
          <button
            v-if="product.stock > 0"
            class="flex items-center justify-center gap-2 bg-brutal-yellow text-brutal-black brutal-border brutal-shadow-sm px-4 py-3 font-bold text-sm uppercase tracking-wide hover:bg-brutal-black hover:text-brutal-yellow transition-all w-full"
            :disabled="adding"
            @click="addToCart"
          >
            <ShoppingBag :size="18" :stroke-width="2.5" />
            {{ added ? '¡Agregado!' : adding ? 'Agregando...' : 'Agregar al carrito' }}
          </button>
          <a
            :href="`https://wa.me/521234567890?text=${whatsappMessage}`"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center justify-center gap-2 bg-whatsapp text-brutal-white brutal-border brutal-shadow-sm px-4 py-3 font-bold text-sm uppercase tracking-wide hover:brightness-110 transition-all w-full"
          >
            <ShoppingBag :size="18" :stroke-width="2.5" />
            Consultar por WhatsApp
          </a>
        </div>
      </div>
    </div>
  </article>
</template>
