<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ShoppingBag, ArrowLeft, Package, Truck, Shield, MessageCircle, Heart, Star } from '@lucide/vue'

import { productsApi, formatPrice, type Product } from '../api/products'
import { useCartStore } from '../stores/cart'
import { useAuthStore } from '../stores/auth'
import { wishlistApi } from '../api/wishlist'
import { ApiError } from '../api/client'

import ProductGallery from '../components/ProductGallery.vue'
import ProductSpecs from '../components/ProductSpecs.vue'
import ProductVariants from '../components/ProductVariants.vue'
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
const activeTab = ref<'reviews' | 'related'>('reviews')

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
  <section class="py-10 sm:py-16 bg-surface-dim min-h-[70vh]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <button
        class="flex items-center gap-2 text-sm text-text-secondary hover:text-text mb-8 transition-colors"
        @click="router.back()"
      >
        <ArrowLeft :size="16" :stroke-width="2" />
        Volver
      </button>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
        <div class="rounded-2xl overflow-hidden">
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

      <!-- Error state -->
      <div v-else-if="error" class="rounded-2xl p-12 text-center max-w-lg mx-auto bg-black/60 backdrop-blur-md border border-red-500/30 shadow-[0_0_15px_rgba(255,59,48,0.1)]">
        <Package :size="48" :stroke-width="1.5" class="mx-auto text-text-secondary mb-4" />
        <h2 class="text-xl font-semibold text-text mb-2">{{ error }}</h2>
        <p class="text-text-secondary text-sm mb-6">El producto que buscas no está disponible o fue eliminado.</p>
        <router-link
          to="/#productos"
          class="btn-primary px-6 py-3 inline-block text-sm"
        >
          Ver catálogo
        </router-link>
      </div>

      <!-- Product content -->
      <div v-else-if="product" class="space-y-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
          <!-- Gallery -->
          <div class="rounded-2xl p-[1px] bg-gradient-to-br from-neon-blue/40 via-transparent to-neon-purple/40 shadow-[0_0_15px_rgba(0,212,255,0.15)]">
            <ProductGallery :image="product.image" :name="product.name" />
          </div>

          <!-- Details -->
          <div class="space-y-6">
            <!-- Breadcrumb -->
            <nav class="text-xs text-text-secondary flex items-center gap-1.5">
              <router-link to="/" class="hover:text-neon-blue hover:drop-shadow-[0_0_6px_rgba(0,212,255,0.5)] transition-all">Home</router-link>
              <span class="text-text-tertiary">›</span>
              <span class="hover:text-neon-blue hover:drop-shadow-[0_0_6px_rgba(0,212,255,0.5)] transition-all cursor-pointer">Categoría</span>
              <span class="text-text-tertiary">›</span>
              <span class="text-text truncate">{{ product.name }}</span>
            </nav>

            <!-- Name + brand -->
            <div>
              <p class="text-secondary text-sm mb-1">{{ product.brand }}</p>
              <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-text" itemprop="name">
                {{ product.name }}
              </h1>
              <p v-if="product.model" class="text-text-secondary text-sm mt-1">
                Modelo: {{ product.model }}
              </p>
            </div>

            <!-- Rating -->
            <div v-if="(product as any).reviews_count" class="flex items-center gap-2">
              <div class="flex items-center gap-0.5">
                <Star
                  v-for="i in 5"
                  :key="i"
                  :size="16"
                  :stroke-width="2"
                  :class="i <= Math.round((product as any).rating ?? 0) ? 'text-amber-400 fill-amber-400' : 'text-border'"
                />
              </div>
              <span class="text-sm text-text-secondary">
                {{ (product as any).rating?.toFixed(1) }}
                <span v-if="(product as any).reviews_count">({{ (product as any).reviews_count }} reseñas)</span>
              </span>
            </div>

            <!-- Price -->
            <div
              itemprop="offers"
              itemscope
              itemtype="https://schema.org/Offer"
              class="flex items-baseline gap-2"
            >
              <span class="text-4xl font-bold text-white drop-shadow-[0_0_8px_rgba(255,255,255,0.15)]">
                <span itemprop="price" :content="String(Number(product.price))">${{ formatPrice(product.price) }}</span>
                <meta itemprop="priceCurrency" content="MXN" />
              </span>
            </div>

            <!-- Stock indicator -->
            <div class="flex items-center gap-2">
              <span
                class="w-2.5 h-2.5 rounded-full"
                :class="inStock ? 'bg-success' : 'bg-red-500'"
              ></span>
              <span class="text-sm font-medium" :class="inStock ? 'text-success' : 'text-red-500'">
                {{ stockLabel }}
              </span>
            </div>

            <!-- Description -->
            <p v-if="product.description" class="text-text-secondary leading-relaxed text-sm">
              {{ product.description }}
            </p>

            <!-- Variants -->
            <ProductVariants :product="product" />

            <!-- Quantity + Add to cart -->
            <div v-if="inStock" class="flex items-center gap-4">
              <label class="text-sm text-text-secondary">Cantidad</label>
              <div class="flex items-center rounded-xl border border-neon-blue/30 overflow-hidden">
                <button
                  class="px-3 py-2 text-text-secondary hover:bg-surface-dim transition-colors text-sm font-medium"
                  :disabled="quantity <= 1"
                  @click="quantity--"
                >
                  −
                </button>
                <span class="px-4 py-2 text-sm font-semibold min-w-[2.5rem] text-center border-x border-neon-blue/30">
                  {{ quantity }}
                </span>
                <button
                  class="px-3 py-2 text-text-secondary hover:bg-surface-dim transition-colors text-sm font-medium"
                  :disabled="quantity >= product.stock"
                  @click="quantity++"
                >
                  +
                </button>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="space-y-3">
              <button
                v-if="inStock"
                class="px-6 py-3.5 w-full flex items-center justify-center gap-2 text-sm font-semibold rounded-full transition-all disabled:opacity-60 bg-neon-blue text-black hover:bg-neon-blue/90 hover:shadow-[0_0_20px_rgba(0,212,255,0.5),0_0_40px_rgba(0,212,255,0.2)] active:scale-[0.98]"
                :disabled="adding"
                @click="addToCart"
              >
                <ShoppingBag :size="18" :stroke-width="2" />
                {{ added ? '¡Agregado!' : adding ? 'Agregando...' : 'Agregar al carrito' }}
              </button>

              <div class="flex gap-3">
                <button
                  class="btn-secondary flex-1 flex items-center justify-center gap-2 py-3 text-sm transition-all"
                  :class="isWishlisted ? 'text-red-500 border-red-200' : ''"
                  :disabled="wishlistLoading"
                  @click="toggleWishlist"
                >
                  <Heart :size="18" :stroke-width="2" :fill="isWishlisted ? 'currentColor' : 'none'" />
                  {{ isWishlisted ? 'Guardado' : 'Favorito' }}
                </button>
                <a
                  :href="`https://wa.me/521234567890?text=${whatsappMessage}`"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn-ghost flex-1 flex items-center justify-center gap-2 py-3 text-sm"
                >
                  <MessageCircle :size="18" :stroke-width="2" />
                  WhatsApp
                </a>
              </div>
            </div>

            <!-- Specs panel (glass) -->
            <div class="rounded-2xl p-6 bg-black/60 backdrop-blur-md border border-neon-blue/20 shadow-[0_0_10px_rgba(0,212,255,0.05)]">
              <ProductSpecs :product="product" />
            </div>

            <!-- Shipping info (glass card) -->
            <div class="rounded-2xl p-4 flex items-start gap-3 bg-black/60 backdrop-blur-md border border-neon-green/20">
              <Truck :size="20" :stroke-width="2" class="text-neon-green mt-0.5 shrink-0" />
              <div class="text-sm">
                <p class="font-medium text-text">Envío a todo México</p>
                <p class="text-text-secondary text-xs mt-0.5">Envío gratis en compras mayores a $999 MXN</p>
              </div>
            </div>

            <div class="rounded-2xl p-4 flex items-start gap-3 bg-black/60 backdrop-blur-md border border-neon-blue/20">
              <Shield :size="20" :stroke-width="2" class="text-neon-blue mt-0.5 shrink-0" />
              <div class="text-sm">
                <p class="font-medium text-text">Garantía incluida</p>
                <p class="text-text-secondary text-xs mt-0.5">3 meses de garantía del fabricante</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="rounded-2xl bg-black/60 backdrop-blur-md border border-border overflow-hidden">
          <div class="flex border-b border-border">
            <button
              class="flex-1 px-6 py-4 text-sm font-semibold uppercase tracking-wide transition-all"
              :class="activeTab === 'reviews' ? 'text-neon-blue border-b-2 border-neon-blue shadow-[0_2px_10px_rgba(0,212,255,0.2)]' : 'text-text-secondary hover:text-text hover:bg-surface-dim'"
              @click="activeTab = 'reviews'"
            >
              Reviews
            </button>
            <button
              class="flex-1 px-6 py-4 text-sm font-semibold uppercase tracking-wide transition-all"
              :class="activeTab === 'related' ? 'text-neon-blue border-b-2 border-neon-blue shadow-[0_2px_10px_rgba(0,212,255,0.2)]' : 'text-text-secondary hover:text-text hover:bg-surface-dim'"
              @click="activeTab = 'related'"
            >
              Relacionados
            </button>
          </div>
          <div class="p-6">
            <ProductReviews v-if="activeTab === 'reviews'" :product-id="product.id" />
            <RelatedProducts v-else :category-id="product.category_id" :current-product-id="product.id" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
