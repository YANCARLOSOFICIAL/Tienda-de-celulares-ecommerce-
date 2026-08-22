<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ShoppingBag, ArrowLeft, Package, Truck, Shield, MessageCircle, Heart } from '@lucide/vue'

import { productsApi, formatPrice, type Product } from '../api/products'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { wishlistApi } from '../api/wishlist'
import { ApiError } from '../api/client'

import ProductGallery from '../components/ProductGallery.vue'
import ProductSpecs from '../components/ProductSpecs.vue'
import ProductReviews from '../components/ProductReviews.vue'
import RelatedProducts from '../components/RelatedProducts.vue'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

const product = ref<Product | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const adding = ref(false)
const added = ref(false)
const quantity = ref(1)
const isWishlisted = ref(false)
const wishlistLoading = ref(false)

const productId = computed(() => Number(route.params.id))

async function fetchProduct() {
  loading.value = true
  error.value = null
  try {
    product.value = await productsApi.get(productId.value)
    checkWishlist()
  } catch (e) {
    if (e instanceof ApiError && e.status === 404) {
      error.value = 'Producto no encontrado'
    } else {
      error.value = 'Error al cargar el producto'
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchProduct)
watch(() => route.params.id, fetchProduct)

let schemaEl: HTMLScriptElement | null = null

function removeSchema() {
  if (schemaEl) {
    schemaEl.remove()
    schemaEl = null
  }
}

function injectSchema(p: Product) {
  removeSchema()
  schemaEl = document.createElement('script')
  schemaEl.type = 'application/ld+json'
  schemaEl.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: p.name,
    image: p.image,
    description: p.description,
    brand: { '@type': 'Brand', name: p.brand },
    model: p.model,
    offers: {
      '@type': 'Offer',
      priceCurrency: 'MXN',
      price: p.price,
      availability: p.stock > 0 ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
    },
  })
  document.head.appendChild(schemaEl)
}

watch(product, (p) => {
  if (p) injectSchema(p)
  else removeSchema()
})

onUnmounted(removeSchema)

const inStock = computed(() => (product.value?.stock ?? 0) > 0)
const stockLabel = computed(() => {
  if (!product.value) return ''
  if (product.value.stock <= 0) return 'Agotado'
  if (product.value.stock <= 5) return `¡Solo quedan ${product.value.stock}!`
  return `${product.value.stock} disponibles`
})

const stockClass = computed(() => {
  if (!product.value) return ''
  if (product.value.stock <= 0) return 'text-red-600 bg-red-50 border-red-300'
  if (product.value.stock <= 5) return 'text-orange-600 bg-orange-50 border-orange-300'
  return 'text-green-700 bg-green-50 border-green-300'
})

const whatsappMessage = computed(() => {
  if (!product.value) return ''
  return encodeURIComponent(
    `¡Hola! Me interesa el ${product.value.name} por $${formatPrice(product.value.price)}. ¿Podrían darme más información?`
  )
})

async function checkWishlist() {
  if (!authStore.isAuthenticated || !product.value) return
  try {
    const items = await wishlistApi.list()
    isWishlisted.value = items.some((i) => i.product_id === product.value!.id)
  } catch { /* ignore */ }
}

async function toggleWishlist() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: `/products/${productId.value}` } })
    return
  }
  if (!product.value) return
  wishlistLoading.value = true
  try {
    if (isWishlisted.value) {
      await wishlistApi.remove(product.value.id)
      isWishlisted.value = false
    } else {
      await wishlistApi.add(product.value.id)
      isWishlisted.value = true
    }
  } catch { /* ignore */ } finally {
    wishlistLoading.value = false
  }
}

async function addToCart() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: `/products/${productId.value}` } })
    return
  }
  if (!inStock.value || !product.value) return
  adding.value = true
  try {
    await cartStore.add(product.value.id, quantity.value)
    added.value = true
    setTimeout(() => (added.value = false), 2500)
  } catch {
    added.value = false
  } finally {
    adding.value = false
  }
}

function buyNow() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: `/products/${productId.value}` } })
    return
  }
  addToCart().then(() => {
    router.push('/checkout')
  })
}
</script>

<template>
  <section class="py-10 sm:py-16 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <button
        class="flex items-center gap-2 text-sm font-bold text-brutal-black/60 hover:text-brutal-black mb-6 transition-colors"
        @click="router.back()"
      >
        <ArrowLeft :size="16" :stroke-width="2.5" />
        Volver
      </button>

      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
        <div class="brutal-card p-0 overflow-hidden">
          <div class="skeleton aspect-square w-full"></div>
        </div>
        <div class="space-y-6">
          <div class="skeleton h-4 w-24"></div>
          <div class="skeleton h-10 w-3/4"></div>
          <div class="skeleton h-8 w-1/3"></div>
          <div class="skeleton h-20 w-full"></div>
          <div class="skeleton h-14 w-full"></div>
        </div>
      </div>

      <div v-else-if="error" class="brutal-card p-12 text-center">
        <Package :size="56" :stroke-width="1.5" class="mx-auto text-brutal-black/30 mb-4" />
        <h2 class="font-black text-2xl uppercase mb-2">{{ error }}</h2>
        <p class="text-brutal-black/60 mb-6">El producto que buscas no está disponible o fue eliminado.</p>
        <router-link
          to="/#productos"
          class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide"
        >
          Ver catálogo
        </router-link>
      </div>

      <div v-else-if="product" class="space-y-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
          <ProductGallery :image="product.image" :name="product.name" />

          <div class="space-y-6">
            <div>
              <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-xs px-3 py-1.5 brutal-border uppercase tracking-wide mb-3">
                {{ product.brand }}
              </span>
              <h1 class="font-black text-3xl sm:text-4xl lg:text-5xl leading-tight uppercase">
                {{ product.name }}
              </h1>
              <p v-if="product.model" class="text-brutal-black/50 text-sm font-semibold mt-1">
                Modelo: {{ product.model }}
              </p>
            </div>

            <div class="flex items-baseline gap-3">
              <span
                class="font-black text-4xl sm:text-5xl"
                itemprop="offers"
                itemscope
                itemtype="https://schema.org/Offer"
              >
                <span itemprop="price" :content="String(Number(product.price))">${{ formatPrice(product.price) }}</span>
                <meta itemprop="priceCurrency" content="MXN" />
              </span>
            </div>

            <div :class="['inline-flex items-center gap-2 px-4 py-2 brutal-border text-sm font-bold', stockClass]">
              <Package :size="16" :stroke-width="2.5" />
              {{ stockLabel }}
            </div>

            <p v-if="product.description" class="text-brutal-black/70 leading-relaxed text-base sm:text-lg">
              {{ product.description }}
            </p>

            <div v-if="inStock" class="flex items-center gap-3">
              <label class="text-sm font-bold">Cantidad:</label>
              <div class="flex items-center brutal-border">
                <button
                  class="px-3 py-2 font-bold text-lg hover:bg-brutal-gray transition-colors"
                  :disabled="quantity <= 1"
                  @click="quantity--"
                >
                  −
                </button>
                <span class="px-4 py-2 font-black text-lg border-x-4 border-brutal-black min-w-[3rem] text-center">
                  {{ quantity }}
                </span>
                <button
                  class="px-3 py-2 font-bold text-lg hover:bg-brutal-gray transition-colors"
                  :disabled="quantity >= product.stock"
                  @click="quantity++"
                >
                  +
                </button>
              </div>
            </div>

            <div class="space-y-3">
              <button
                v-if="inStock"
                class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-4 w-full flex items-center justify-center gap-2 uppercase tracking-wide text-base disabled:opacity-60"
                :disabled="adding"
                @click="addToCart"
              >
                <ShoppingBag :size="20" :stroke-width="2.5" />
                {{ added ? '¡Agregado al carrito!' : adding ? 'Agregando...' : 'Agregar al carrito' }}
              </button>

              <button
                class="brutal-button px-6 py-4 w-full flex items-center justify-center gap-2 uppercase tracking-wide text-base"
                :class="isWishlisted ? 'bg-red-100 text-red-600' : 'bg-brutal-white text-brutal-black'"
                :disabled="wishlistLoading"
                @click="toggleWishlist"
              >
                <Heart :size="20" :stroke-width="2.5" :fill="isWishlisted ? 'currentColor' : 'none'" />
                {{ isWishlisted ? 'En favoritos' : 'Agregar a favoritos' }}
              </button>

              <a
                :href="`https://wa.me/521234567890?text=${whatsappMessage}`"
                target="_blank"
                rel="noopener noreferrer"
                class="brutal-button bg-whatsapp text-brutal-white px-6 py-4 w-full flex items-center justify-center gap-2 uppercase tracking-wide text-base"
              >
                <MessageCircle :size="20" :stroke-width="2.5" />
                Consultar por WhatsApp
              </a>
            </div>

            <div class="border-t-4 border-brutal-black pt-6 space-y-3">
              <div class="flex items-center gap-3 text-sm text-brutal-black/60">
                <Truck :size="18" :stroke-width="2" class="text-brutal-black/40" />
                <span class="font-semibold">Envío a todo México</span>
              </div>
              <div class="flex items-center gap-3 text-sm text-brutal-black/60">
                <Shield :size="18" :stroke-width="2" class="text-brutal-black/40" />
                <span class="font-semibold">Garantía incluida</span>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-1">
            <ProductSpecs :product="product" />
          </div>
          <div class="lg:col-span-2">
            <div v-if="product.description" class="brutal-card p-5 sm:p-6">
              <h3 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
                <span class="bg-brutal-yellow p-1.5 brutal-border text-xs">📝</span>
                Descripción
              </h3>
              <p class="text-brutal-black/70 leading-relaxed whitespace-pre-line">{{ product.description }}</p>
            </div>
          </div>
        </div>

        <div class="mt-12">
          <ProductReviews :product-id="product.id" />
        </div>

        <RelatedProducts :category-id="product.category_id" :current-product-id="product.id" />
      </div>
    </div>
  </section>
</template>
