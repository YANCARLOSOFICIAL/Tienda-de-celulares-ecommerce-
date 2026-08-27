import { ref } from 'vue'
import { defineStore } from 'pinia'

import { cartApi, type Cart } from '@/api/cart'
import { ApiError } from '@/api/client'

export const useCartStore = defineStore('cart', () => {
  const cart = ref<Cart | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const itemCount = ref(0)

  function applyCart(data: Cart) {
    cart.value = data
    itemCount.value = data.item_count
  }

  async function fetchCart() {
    loading.value = true
    error.value = null
    try {
      applyCart(await cartApi.get())
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        cart.value = null
        itemCount.value = 0
      } else {
        error.value = e instanceof Error ? e.message : 'Error al cargar el carrito'
      }
    } finally {
      loading.value = false
    }
  }

  async function add(productId: number, quantity = 1) {
    error.value = null
    const item = await cartApi.addItem(productId, quantity)
    if (cart.value) {
      const existing = cart.value.items.find((i) => i.product_id === productId)
      if (existing) {
        existing.quantity += quantity
        existing.subtotal = item.subtotal
      } else {
        cart.value.items.push(item)
      }
      itemCount.value = cart.value.items.reduce((acc, i) => acc + i.quantity, 0)
    } else {
      await fetchCart()
    }
  }

  async function updateQuantity(itemId: number, quantity: number) {
    error.value = null
    const updated = await cartApi.updateItem(itemId, quantity)
    if (cart.value) {
      const index = cart.value.items.findIndex((i) => i.id === itemId)
      if (index !== -1) cart.value.items[index] = updated
      itemCount.value = cart.value.items.reduce((acc, i) => acc + i.quantity, 0)
    }
  }

  async function remove(itemId: number) {
    error.value = null
    await cartApi.removeItem(itemId)
    if (cart.value) {
      cart.value.items = cart.value.items.filter((i) => i.id !== itemId)
      itemCount.value = cart.value.items.reduce((acc, i) => acc + i.quantity, 0)
    }
  }

  async function clear() {
    error.value = null
    await cartApi.clear()
    if (cart.value) {
      cart.value.items = []
      cart.value.total = '0.00'
      itemCount.value = 0
    }
  }

  return { cart, loading, error, itemCount, fetchCart, add, updateQuantity, remove, clear }
})
