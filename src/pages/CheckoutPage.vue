<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { CheckCircle2, ShoppingBag, XCircle } from '@lucide/vue'

import { formatPrice } from '../api/products'
import { ordersApi, orderStatusLabels } from '../api/orders'
import { ApiError } from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const processing = ref(false)
const orderError = ref<string | null>(null)
const createdOrderId = ref<number | null>(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/checkout' } })
    return
  }
  await cartStore.fetchCart()
})

const items = computed(() => cartStore.cart?.items ?? [])
const isEmpty = computed(() => items.value.length === 0)
const total = computed(() => cartStore.cart?.total ?? '0')

async function placeOrder() {
  processing.value = true
  orderError.value = null
  try {
    const order = await ordersApi.create()
    createdOrderId.value = order.id
    await cartStore.fetchCart()
  } catch (e) {
    if (e instanceof ApiError) {
      orderError.value = e.message
    } else {
      orderError.value = 'Ocurrió un error al procesar el pedido.'
    }
  } finally {
    processing.value = false
  }
}
</script>

<template>
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-10">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <ShoppingBag :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Confirmar pedido</h1>
      </div>

      <div v-if="createdOrderId" class="brutal-card p-10 text-center">
        <CheckCircle2 :size="56" :stroke-width="2" class="mx-auto text-green-600 mb-4" />
        <h2 class="font-black text-2xl uppercase mb-2">¡Pedido creado!</h2>
        <p class="text-brutal-black/70 mb-6">
          Tu pedido #{{ createdOrderId }} fue registrado con éxito. Hemos descontado el inventario y
          puedes darle seguimiento desde tus pedidos.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <router-link to="/orders" class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 uppercase tracking-wide">
            Ver mis pedidos
          </router-link>
          <router-link to="/#productos" class="brutal-button bg-brutal-white text-brutal-black px-6 py-3 uppercase tracking-wide">
            Seguir comprando
          </router-link>
        </div>
      </div>

      <div v-else-if="cartStore.loading" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg">Cargando carrito...</p>
      </div>

      <div v-else-if="isEmpty" class="brutal-card p-10 text-center">
        <p class="font-black text-2xl uppercase mb-4">No hay productos en tu carrito</p>
        <router-link to="/#productos" class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide">
          Ver catálogo
        </router-link>
      </div>

      <div v-else class="space-y-6">
        <div class="brutal-card overflow-hidden">
          <div
            v-for="item in items"
            :key="item.id"
            class="flex items-center justify-between gap-4 p-5 border-b-4 border-brutal-black last:border-b-0"
          >
            <div class="min-w-0">
              <h3 class="font-black leading-tight">{{ item.product.name }}</h3>
              <p class="text-sm text-brutal-black/60">
                ${{ formatPrice(item.product.price) }} × {{ item.quantity }}
              </p>
            </div>
            <span class="font-black whitespace-nowrap">${{ formatPrice(item.subtotal) }}</span>
          </div>
        </div>

        <div class="brutal-card p-5">
          <div class="flex justify-between items-center mb-4">
            <span class="font-black text-xl uppercase">Total</span>
            <span class="font-black text-2xl">${{ formatPrice(total) }}</span>
          </div>
          <p class="text-sm text-brutal-black/60 mb-4">
            Al confirmar se creará tu pedido, se descontará el inventario y se vaciará tu carrito.
            El estado inicial será <strong>{{ orderStatusLabels.PENDING }}</strong>.
          </p>

          <p v-if="orderError" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm mb-4 flex items-center gap-2">
            <XCircle :size="18" :stroke-width="2.5" />
            {{ orderError }}
          </p>

          <button
            class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-4 w-full flex items-center justify-center gap-2 uppercase tracking-wide disabled:opacity-60"
            :disabled="processing"
            @click="placeOrder"
          >
            <ShoppingBag :size="18" :stroke-width="2.5" />
            {{ processing ? 'Procesando...' : 'Confirmar pedido' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
