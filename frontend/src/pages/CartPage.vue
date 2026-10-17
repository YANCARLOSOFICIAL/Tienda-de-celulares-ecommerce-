<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Minus, Plus, ShoppingCart, Trash2, X } from '@lucide/vue'

import { formatPrice } from '@/api/products'
import { ApiError } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useToast } from '@/composables/useToast'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const toast = useToast()

function toastError(e: unknown, fallback: string) {
  toast.error(e instanceof ApiError ? e.message : fallback)
}

async function changeQuantity(itemId: number, quantity: number) {
  try {
    await cartStore.updateQuantity(itemId, quantity)
  } catch (e) {
    toastError(e, 'No se pudo actualizar la cantidad')
  }
}

async function removeItem(itemId: number) {
  try {
    await cartStore.remove(itemId)
    toast.success('Producto eliminado del carrito')
  } catch (e) {
    toastError(e, 'No se pudo eliminar el producto')
  }
}

async function clearCart() {
  try {
    await cartStore.clear()
    toast.success('Carrito vaciado')
  } catch (e) {
    toastError(e, 'No se pudo vaciar el carrito')
  }
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/cart' } })
    return
  }
  await cartStore.fetchCart()
})

const items = computed(() => cartStore.cart?.items ?? [])
const isEmpty = computed(() => items.value.length === 0)
</script>

<template>
  <section class="page">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="page-header mb-10">
        <p class="eyebrow">Selección</p>
        <h1 class="page-title flex items-center gap-3">
          <ShoppingCart :size="26" :stroke-width="1.75" class="text-accent" />
          Mi carrito
        </h1>
      </div>

      <div v-if="cartStore.loading" class="maison-panel p-12 text-center">
        <p class="font-medium text-text">Cargando carrito...</p>
      </div>

      <div v-else-if="isEmpty" class="maison-panel p-14 text-center">
        <ShoppingCart :size="44" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-5" />
        <p class="text-display text-xl text-accent mb-3">Tu carrito está vacío</p>
        <p class="text-text-secondary mb-8">Agrega productos del catálogo para comenzar tu compra.</p>
        <router-link to="/shop" class="btn-fill">
          Ver catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col lg:flex-row gap-6">
        <div class="flex-1 space-y-3">
          <div
            v-for="item in items"
            :key="item.id"
            class="maison-panel p-4 flex flex-col sm:flex-row items-start sm:items-center gap-4"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/f5f0e6/0a0906?text=Producto&font=inter'"
              :alt="item.product.name"
              class="w-20 h-20 object-cover flex-shrink-0 border border-border"
            />
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-base text-text leading-tight" style="font-family: var(--font-family-serif);">{{ item.product.name }}</h3>
              <p class="text-xs uppercase tracking-[0.14em] text-text-tertiary mt-1">{{ item.product.brand }}</p>
              <p class="font-medium mt-1.5 text-accent text-sm">${{ formatPrice(item.product.price) }}</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                class="qty-mini"
                :disabled="item.quantity <= 1"
                aria-label="Disminuir cantidad"
                @click="changeQuantity(item.id, item.quantity - 1)"
              >
                <Minus :size="14" :stroke-width="2" />
              </button>
              <span class="font-medium text-sm w-9 text-center text-text">
                {{ item.quantity }}
              </span>
              <button
                class="qty-mini"
                :disabled="item.quantity >= item.product.stock"
                aria-label="Aumentar cantidad"
                @click="changeQuantity(item.id, item.quantity + 1)"
              >
                <Plus :size="14" :stroke-width="2" />
              </button>
            </div>

            <div class="flex items-center gap-4 sm:w-40 sm:justify-end">
              <span class="font-semibold text-base text-text">${{ formatPrice(item.subtotal) }}</span>
              <button
                class="p-2 text-danger hover:bg-danger/10 transition-colors"
                aria-label="Eliminar producto"
                @click="removeItem(item.id)"
              >
                <Trash2 :size="16" :stroke-width="2" />
              </button>
            </div>
          </div>
        </div>

        <div class="lg:w-80">
          <div class="maison-panel p-6 sticky top-24">
            <p class="eyebrow mb-5">Resumen</p>
            <div class="flex justify-between text-sm text-text-secondary mb-2">
              <span>Artículos</span>
              <span>{{ cartStore.itemCount }}</span>
            </div>
            <div class="flex justify-between font-semibold text-xl text-text mb-6 pb-4 border-b border-border">
              <span>Total</span>
              <span class="text-accent">${{ formatPrice(cartStore.cart?.total ?? '0') }}</span>
            </div>
            <router-link
              to="/checkout"
              class="btn-fill w-full"
            >
              Proceder al pago
            </router-link>
            <button
              class="btn-ghost w-full justify-center mt-3 text-text-tertiary hover:text-danger"
              @click="clearCart()"
            >
              <X :size="15" :stroke-width="2" />
              Vaciar carrito
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.qty-mini {
  width: 34px;
  height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  background: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
}

.qty-mini:hover:not(:disabled) {
  color: var(--color-accent);
  border-color: rgba(240, 196, 25, 0.4);
}

.qty-mini:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
</style>
