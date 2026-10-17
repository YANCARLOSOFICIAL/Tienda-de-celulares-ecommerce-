<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ShoppingBag, ArrowLeft, Package, Truck, Shield, MessageCircle, Heart, Star } from '@lucide/vue'

import { productsApi, formatPrice, type Product } from '@/api/products'
import { site, whatsappProductUrl, formatCurrency } from '@/config/site'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { wishlistApi } from '@/api/wishlist'
import { ApiError } from '@/api/client'
import { useToast } from '@/composables/useToast'

import ProductGallery from '@/components/product/ProductGallery.vue'
import ProductSpecs from '@/components/product/ProductSpecs.vue'
import ProductVariants from '@/components/product/ProductVariants.vue'
import ProductReviews from '@/components/product/ProductReviews.vue'
import RelatedProducts from '@/components/product/RelatedProducts.vue'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const toast = useToast()

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
    image: p.images?.length ? p.images : p.image,
    description: p.description,
    brand: { '@type': 'Brand', name: p.brand },
    model: p.model,
    offers: {
      '@type': 'Offer',
      priceCurrency: site.currency,
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

const whatsappHref = computed(() =>
  product.value ? whatsappProductUrl(product.value.name, product.value.price) : '#',
)

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
      toast.success('Quitado de favoritos')
    } else {
      await wishlistApi.add(product.value.id)
      isWishlisted.value = true
      toast.success('Agregado a favoritos')
    }
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'No se pudo actualizar favoritos')
  } finally {
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
    toast.success(`${product.value.name} se agregó al carrito`)
    setTimeout(() => (added.value = false), 2500)
  } catch (e) {
    added.value = false
    toast.error(e instanceof ApiError ? e.message : 'No se pudo agregar al carrito')
    throw e
  } finally {
    adding.value = false
  }
}

async function buyNow() {
  if (!authStore.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: `/products/${productId.value}` } })
    return
  }
  try {
    await addToCart()
    router.push('/checkout')
  } catch {
    /* el error ya se notificó en addToCart */
  }
}
</script>

<template>
  <section class="page">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <button
        class="flex items-center gap-2 text-[12px] uppercase tracking-[0.14em] text-text-secondary hover:text-accent mb-8 transition-colors"
        @click="router.back()"
      >
        <ArrowLeft :size="15" :stroke-width="2" />
        Volver
      </button>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">
        <div class="overflow-hidden border border-border">
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
      <div v-else-if="error" class="maison-panel p-16 text-center max-w-lg mx-auto">
        <Package :size="44" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-5" />
        <h2 class="text-display text-2xl mb-3">{{ error }}</h2>
        <p class="text-text-secondary text-sm mb-8">El producto que buscas no está disponible o fue eliminado.</p>
        <router-link to="/shop" class="btn-fill">
          Ver catálogo
        </router-link>
      </div>

      <!-- Product content -->
      <div v-else-if="product" class="space-y-14">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-14">
          <!-- Gallery -->
          <div class="overflow-hidden border border-border">
            <ProductGallery :image="product.image" :images="product.images" :name="product.name" />
          </div>

          <!-- Details -->
          <div class="space-y-6">
            <!-- Breadcrumb -->
            <nav class="text-[11px] uppercase tracking-[0.16em] text-text-tertiary flex items-center gap-2" style="font-family: var(--font-family-mono);">
              <router-link to="/" class="hover:text-accent transition-colors">Home</router-link>
              <span>›</span>
              <router-link to="/shop" class="hover:text-accent transition-colors">Tienda</router-link>
              <span>›</span>
              <span class="text-text truncate">{{ product.name }}</span>
            </nav>

            <!-- Name + brand -->
            <div>
              <span class="tag mb-3 inline-block">{{ product.brand }}</span>
              <h1 class="text-display text-3xl sm:text-4xl" itemprop="name">
                {{ product.name }}
              </h1>
              <p v-if="product.model" class="text-text-secondary text-sm mt-2">
                Modelo: {{ product.model }}
              </p>
            </div>

            <!-- Rating -->
            <div v-if="(product as any).reviews_count" class="flex items-center gap-2">
              <div class="flex items-center gap-0.5">
                <Star
                  v-for="i in 5"
                  :key="i"
                  :size="15"
                  :stroke-width="1.75"
                  :class="i <= Math.round((product as any).rating ?? 0) ? 'text-accent fill-[#f0c419]' : 'text-text-tertiary'"
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
              <span class="product-price-lg">
                <span itemprop="price" :content="String(Number(product.price))">${{ formatPrice(product.price) }}</span>
                <meta itemprop="priceCurrency" :content="site.currency" />
              </span>
            </div>

            <!-- Stock indicator -->
            <div class="flex items-center gap-2.5">
              <span
                class="w-2 h-2"
                :class="inStock ? 'bg-success' : 'bg-danger'"
              ></span>
              <span class="text-sm font-medium" :class="inStock ? 'text-success' : 'text-danger'">
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
              <label class="eyebrow">Cantidad</label>
              <div class="qty-stepper">
                <button
                  class="qty-btn"
                  :disabled="quantity <= 1"
                  @click="quantity--"
                >
                  −
                </button>
                <span class="qty-value">{{ quantity }}</span>
                <button
                  class="qty-btn"
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
                class="btn-fill w-full"
                :disabled="adding"
                @click="addToCart"
              >
                <ShoppingBag :size="17" :stroke-width="2" />
                {{ added ? '¡Agregado!' : adding ? 'Agregando...' : 'Agregar al carrito' }}
              </button>

              <div class="flex gap-3">
                <button
                  class="btn-outline flex-1"
                  :class="isWishlisted ? 'text-[#ef4444] border-[#ef4444]/40' : ''"
                  :disabled="wishlistLoading"
                  @click="toggleWishlist"
                >
                  <Heart :size="16" :stroke-width="2" :fill="isWishlisted ? 'currentColor' : 'none'" />
                  {{ isWishlisted ? 'Guardado' : 'Favorito' }}
                </button>
                <a
                  :href="whatsappHref"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn-outline flex-1"
                >
                  <MessageCircle :size="16" :stroke-width="2" />
                  WhatsApp
                </a>
              </div>
            </div>

            <!-- Specs panel -->
            <div class="maison-panel p-6">
              <ProductSpecs :product="product" />
            </div>

            <!-- Shipping info -->
            <div class="maison-panel p-5 flex items-start gap-4">
              <Truck :size="20" :stroke-width="1.75" class="text-accent mt-0.5 shrink-0" />
              <div class="text-sm">
                <p class="font-medium text-text">Envío a todo {{ site.country }}</p>
                <p class="text-text-secondary text-xs mt-1">Envío estándar gratis en compras superiores a {{ formatCurrency(site.freeShippingThreshold) }}</p>
              </div>
            </div>

            <div class="maison-panel p-5 flex items-start gap-4">
              <Shield :size="20" :stroke-width="1.75" class="text-accent mt-0.5 shrink-0" />
              <div class="text-sm">
                <p class="font-medium text-text">Garantía incluida</p>
                <p class="text-text-secondary text-xs mt-1">1 año de garantía del fabricante</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="border border-border">
          <div class="flex border-b border-border">
            <button
              class="tab-btn"
              :class="activeTab === 'reviews' ? 'tab-active' : ''"
              @click="activeTab = 'reviews'"
            >
              Reseñas
            </button>
            <button
              class="tab-btn"
              :class="activeTab === 'related' ? 'tab-active' : ''"
              @click="activeTab = 'related'"
            >
              Relacionados
            </button>
          </div>
          <div class="p-6 sm:p-8">
            <ProductReviews v-if="activeTab === 'reviews'" :product-id="product.id" />
            <RelatedProducts v-else :category-id="product.category_id" :current-product-id="product.id" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.product-price-lg {
  font-family: var(--font-family-serif);
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 600;
  color: var(--color-accent);
  line-height: 1;
}

.qty-stepper {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border-strong);
  background: var(--color-surface-dim);
}

.qty-btn {
  width: 44px;
  height: 44px;
  font-size: 17px;
  color: var(--color-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.2s ease, background 0.2s ease;
}

.qty-btn:hover:not(:disabled) {
  color: var(--color-accent);
  background: rgba(240, 196, 25, 0.06);
}

.qty-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.qty-value {
  min-width: 48px;
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  border-left: 1px solid var(--color-border-strong);
  border-right: 1px solid var(--color-border-strong);
  padding: 10px 0;
}

.tab-btn {
  flex: 1;
  padding: 18px 24px;
  font-family: var(--font-family-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  cursor: pointer;
  transition: color 0.25s ease, border-color 0.25s ease;
}

.tab-btn:hover {
  color: var(--color-text-secondary);
}

.tab-active {
  color: var(--color-accent);
  border-bottom-color: var(--color-accent);
}
</style>
