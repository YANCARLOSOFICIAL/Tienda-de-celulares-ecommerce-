import { defineStore } from 'pinia'
import { ref } from 'vue'

import { productsApi, type Product, type ProductFilters, type ProductPage } from '@/api/products'

export type { Product } from '@/api/products'

export const useProductsStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const total = ref(0)
  const page = ref(1)
  const pageSize = ref(12)
  const pages = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProducts(filters: ProductFilters = {}) {
    loading.value = true
    error.value = null
    try {
      const data: ProductPage = await productsApi.list({
        page: page.value,
        page_size: pageSize.value,
        ...filters,
      })
      products.value = data.items
      total.value = data.total
      pages.value = data.pages
      page.value = data.page
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Ocurrió un error al cargar los productos.'
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    total,
    page,
    pageSize,
    pages,
    loading,
    error,
    fetchProducts,
  }
})
