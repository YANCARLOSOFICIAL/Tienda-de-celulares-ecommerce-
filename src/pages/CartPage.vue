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
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <ShoppingCart :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Mi carrito</h1>
      </div>

      <div v-if="cartStore.loading" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg">Cargando carrito...</p>
      </div>

      <div v-else-if="isEmpty" class="brutal-card p-10 text-center">
        <p class="font-black text-2xl uppercase mb-4">Tu carrito está vacío</p>
        <p class="text-brutal-black/60 mb-6">Agrega productos del catálogo para comenzar tu compra.</p>
        <router-link to="/#productos" class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide">
          Ver catálogo
        </router-link>
      </div>

      <div v-else class="space-y-6">
        <div class="brutal-card overflow-hidden">
          <div
            v-for="item in items"
            :key="item.id"
            class="flex flex-col sm:flex-row items-start sm:items-center gap-4 p-5 border-b-4 border-brutal-black last:border-b-0"
          >
            <img
              :src="item.product.image || 'https://placehold.co/200x200/111111/FFD60A?text=Producto&font=inter'"
              :alt="item.product.name"
              class="w-20 h-20 object-cover brutal-border flex-shrink-0"
            />
            <div class="flex-1 min-w-0">
              <h3 class="font-black text-lg leading-tight">{{ item.product.name }}</h3>
              <p class="text-sm text-brutal-black/60">{{ item.product.brand }}</p>
              <p class="font-black mt-1">${{ formatPrice(item.product.price) }}</p>
            </div>

            <div class="flex items-center gap-2">
              <button
                class="brutal-border p-2 bg-brutal-white hover:bg-brutal-yellow transition-colors"
                :disabled="item.quantity <= 1"
                aria-label="Disminuir cantidad"
                @click="cartStore.updateQuantity(item.id, item.quantity - 1)"
              >
                <Minus :size="16" :stroke-width="2.5" />
              </button>
              <span class="font-black text-lg w-10 text-center brutal-border py-1 bg-brutal-white">
                {{ item.quantity }}
              </span>
              <button
                class="brutal-border p-2 bg-brutal-white hover:bg-brutal-yellow transition-colors"
                :disabled="item.quantity >= item.product.stock"
                aria-label="Aumentar cantidad"
                @click="cartStore.updateQuantity(item.id, item.quantity + 1)"
              >
                <Plus :size="16" :stroke-width="2.5" />
              </button>
            </div>

            <div class="flex items-center gap-4 sm:w-40 sm:justify-end">
              <span class="font-black text-lg">${{ formatPrice(item.subtotal) }}</span>
              <button
                class="brutal-border p-2 bg-red-100 hover:bg-red-200 transition-colors"
                aria-label="Eliminar producto"
                @click="cartStore.remove(item.id)"
              >
                <Trash2 :size="16" :stroke-width="2.5" class="text-red-700" />
              </button>
            </div>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <button
            class="brutal-button bg-brutal-white text-brutal-black px-5 py-3 flex items-center justify-center gap-2 uppercase tracking-wide"
            @click="cartStore.clear()"
          >
            <X :size="18" :stroke-width="2.5" />
            Vaciar carrito
          </button>

          <div class="brutal-card p-5 sm:min-w-[280px]">
            <div class="flex justify-between font-bold mb-1">
              <span class="uppercase text-sm">Artículos</span>
              <span>{{ cartStore.itemCount }}</span>
            </div>
            <div class="flex justify-between font-black text-xl mb-4">
              <span class="uppercase">Total</span>
              <span>${{ formatPrice(cartStore.cart?.total ?? '0') }}</span>
            </div>
            <router-link
              to="/checkout"
              class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-4 w-full flex items-center justify-center gap-2 uppercase tracking-wide"
            >
              Proceder al pago
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
