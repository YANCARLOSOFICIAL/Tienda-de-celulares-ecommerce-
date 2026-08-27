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
  <section class="py-16 sm:py-20 bg-surface min-h-[70vh]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <ShoppingCart :size="24" :stroke-width="2" class="text-white" />
        <h1 class="font-semibold text-2xl sm:text-3xl text-text" style="font-family: var(--font-family-serif);">Mi carrito</h1>
      </div>

      <div v-if="cartStore.loading" class="bento-card p-10 text-center bg-surface-dim border border-border rounded-2xl">
        <p class="font-medium text-white">Cargando carrito...</p>
      </div>

      <div v-else-if="isEmpty" class="bento-card p-10 text-center bg-surface-dim border border-border rounded-2xl">
        <ShoppingCart :size="48" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-4" />
        <p class="font-semibold text-xl text-gold mb-2">Tu carrito está vacío</p>
        <p class="text-text-secondary mb-6">Agrega productos del catálogo para comenzar tu compra.</p>
        <router-link to="/#productos" class="btn-gold px-6 py-3 inline-block">
          Ver catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col lg:flex-row gap-6">
        <div class="flex-1 space-y-3">
          <div
            v-for="item in items"
            :key="item.id"
            class="bento-card p-4 flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-surface-dim border border-border rounded-2xl"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/FAFAFA/1D1D1F?text=Producto&font=inter'"
              :alt="item.product.name"
              class="w-20 h-20 object-cover rounded-xl flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-base text-white leading-tight">{{ item.product.name }}</h3>
              <p class="text-sm text-text-secondary">{{ item.product.brand }}</p>
              <p class="font-semibold mt-1 text-gold">${{ formatPrice(item.product.price) }}</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                class="input-minimal p-2 hover:bg-white/5 transition-colors rounded-lg border border-white/10"
                :disabled="item.quantity <= 1"
                aria-label="Disminuir cantidad"
                @click="changeQuantity(item.id, item.quantity - 1)"
              >
                <Minus :size="16" :stroke-width="2" />
              </button>
              <span class="font-semibold text-sm w-10 text-center text-white">
                {{ item.quantity }}
              </span>
              <button
                class="input-minimal p-2 hover:bg-white/5 transition-colors rounded-lg border border-white/10"
                :disabled="item.quantity >= item.product.stock"
                aria-label="Aumentar cantidad"
                @click="changeQuantity(item.id, item.quantity + 1)"
              >
                <Plus :size="16" :stroke-width="2" />
              </button>
            </div>

            <div class="flex items-center gap-4 sm:w-40 sm:justify-end">
              <span class="font-semibold text-base text-white">${{ formatPrice(item.subtotal) }}</span>
              <button
                class="p-2 text-red-400 hover:bg-red-400/10 transition-colors rounded-lg"
                aria-label="Eliminar producto"
                @click="removeItem(item.id)"
              >
                <Trash2 :size="16" :stroke-width="2" />
              </button>
            </div>
          </div>
        </div>

        <div class="lg:w-80">
          <div class="bento-card p-6 sticky top-24 bg-surface-dim border border-border rounded-2xl">
            <div class="flex justify-between text-sm text-text-secondary mb-2">
              <span>Artículos</span>
              <span>{{ cartStore.itemCount }}</span>
            </div>
            <div class="flex justify-between font-semibold text-xl text-white mb-6 pb-4 border-b border-white/10">
              <span>Total</span>
              <span class="text-gold">${{ formatPrice(cartStore.cart?.total ?? '0') }}</span>
            </div>
            <router-link
              to="/checkout"
              class="btn-gold px-6 py-3 w-full flex items-center justify-center gap-2 transition-shadow"
            >
              Proceder al pago
            </router-link>
            <button
              class="btn-ghost mt-3 w-full flex items-center justify-center gap-2 text-sm text-text-tertiary hover:text-white hover:bg-white/5"
              @click="clearCart()"
            >
              <X :size="16" :stroke-width="2" />
              Vaciar carrito
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
