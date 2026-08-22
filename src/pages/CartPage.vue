<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Minus, Plus, ShoppingCart, Trash2, X } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

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
  <section class="py-16 sm:py-20 bg-[#0a0a0f] min-h-[70vh]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <ShoppingCart :size="24" :stroke-width="2" class="text-text" />
        <h1 class="font-semibold text-2xl sm:text-3xl text-text">Mi carrito</h1>
      </div>

      <div v-if="cartStore.loading" class="bento-card p-10 text-center bg-[#111118]/80 backdrop-blur-xl border border-[#00f0ff]/20">
        <p class="font-medium text-[#e0e0e8]">Cargando carrito...</p>
      </div>

      <div v-else-if="isEmpty" class="bento-card p-10 text-center bg-[#111118]/80 backdrop-blur-xl border border-[#00f0ff]/20">
        <ShoppingCart :size="48" :stroke-width="1.5" class="mx-auto text-[#8a8a9a] mb-4" />
        <p class="font-semibold text-xl text-[#00f0ff] mb-2">Tu carrito está vacío</p>
        <p class="text-[#8a8a9a] mb-6">Agrega productos del catálogo para comenzar tu compra.</p>
        <router-link to="/#productos" class="btn-primary px-6 py-3 inline-block">
          Ver catálogo
        </router-link>
      </div>

      <div v-else class="flex flex-col lg:flex-row gap-6">
        <div class="flex-1 space-y-3">
          <div
            v-for="item in items"
            :key="item.id"
            class="bento-card p-4 flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-[#111118]/80 backdrop-blur-xl border border-[#00f0ff]/20"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/FAFAFA/1D1D1F?text=Producto&font=inter'"
              :alt="item.product.name"
              class="w-20 h-20 object-cover rounded-xl flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-base text-[#e0e0e8] leading-tight">{{ item.product.name }}</h3>
              <p class="text-sm text-[#8a8a9a]">{{ item.product.brand }}</p>
              <p class="font-semibold mt-1 text-[#00f0ff]">${{ formatPrice(item.product.price) }}</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                class="input-minimal p-2 hover:bg-[#00f0ff]/10 transition-colors rounded-lg border border-[#00f0ff]/30"
                :disabled="item.quantity <= 1"
                aria-label="Disminuir cantidad"
                @click="cartStore.updateQuantity(item.id, item.quantity - 1)"
              >
                <Minus :size="16" :stroke-width="2" />
              </button>
              <span class="font-semibold text-sm w-10 text-center text-[#e0e0e8]">
                {{ item.quantity }}
              </span>
              <button
                class="input-minimal p-2 hover:bg-[#00f0ff]/10 transition-colors rounded-lg border border-[#00f0ff]/30"
                :disabled="item.quantity >= item.product.stock"
                aria-label="Aumentar cantidad"
                @click="cartStore.updateQuantity(item.id, item.quantity + 1)"
              >
                <Plus :size="16" :stroke-width="2" />
              </button>
            </div>

            <div class="flex items-center gap-4 sm:w-40 sm:justify-end">
              <span class="font-semibold text-base text-[#e0e0e8]">${{ formatPrice(item.subtotal) }}</span>
              <button
                class="p-2 text-[#ff3b3b] hover:bg-[#ff3b3b]/10 transition-colors rounded-lg hover:shadow-[0_0_12px_rgba(255,59,59,0.5)]"
                aria-label="Eliminar producto"
                @click="cartStore.remove(item.id)"
              >
                <Trash2 :size="16" :stroke-width="2" />
              </button>
            </div>
          </div>
        </div>

        <div class="lg:w-80">
          <div class="bento-card p-6 sticky top-24 bg-[#111118]/80 backdrop-blur-xl border border-[#00f0ff]/20">
            <div class="flex justify-between text-sm text-[#8a8a9a] mb-2">
              <span>Artículos</span>
              <span>{{ cartStore.itemCount }}</span>
            </div>
            <div class="flex justify-between font-semibold text-xl text-[#e0e0e8] mb-6 pb-4 border-b border-[#00f0ff]/30">
              <span>Total</span>
              <span class="text-[#00f0ff]">${{ formatPrice(cartStore.cart?.total ?? '0') }}</span>
            </div>
            <router-link
              to="/checkout"
              class="btn-primary px-6 py-3 w-full flex items-center justify-center gap-2 bg-[#00f0ff] hover:shadow-[0_0_20px_rgba(0,240,255,0.5)] transition-shadow"
            >
              Proceder al pago
            </router-link>
            <button
              class="btn-ghost mt-3 w-full flex items-center justify-center gap-2 text-sm text-[#8a8a9a] hover:text-[#e0e0e8] hover:bg-[#00f0ff]/10"
              @click="cartStore.clear()"
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
