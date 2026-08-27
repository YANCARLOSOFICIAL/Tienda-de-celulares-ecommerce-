import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Product } from '@/api/products'

const MAX_COMPARE = 3

export const useCompareStore = defineStore('compare', () => {
  const items = ref<Product[]>([])

  const count = computed(() => items.value.length)
  const isFull = computed(() => items.value.length >= MAX_COMPARE)

  function add(product: Product) {
    if (isFull.value) return false
    if (items.value.some(p => p.id === product.id)) return false
    items.value.push(product)
    return true
  }

  function remove(productId: number) {
    items.value = items.value.filter(p => p.id !== productId)
  }

  function toggle(product: Product) {
    if (items.value.some(p => p.id === product.id)) {
      remove(product.id)
      return false
    }
    return add(product)
  }

  function isInCompare(productId: number) {
    return items.value.some(p => p.id === productId)
  }

  function clear() {
    items.value = []
  }

  return {
    items,
    count,
    isFull,
    add,
    remove,
    toggle,
    isInCompare,
    clear,
  }
})