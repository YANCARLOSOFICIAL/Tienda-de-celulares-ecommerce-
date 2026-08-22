<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, SlidersHorizontal, X, ChevronDown } from '@lucide/vue'

import { productsApi, type Product, type ProductFilters } from '../api/products'
import { categoriesApi, type Category } from '../api/categories'
import ProductCard from '../components/ProductCard.vue'

const route = useRoute()
const router = useRouter()

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const total = ref(0)
const pages = ref(0)

const search = ref((route.query.search as string) || '')
const selectedCategory = ref<number | undefined>(
  route.query.category_id ? Number(route.query.category_id) : undefined
)
const selectedBrand = ref((route.query.brand as string) || '')
const minPrice = ref((route.query.min_price as string) || '')
const maxPrice = ref((route.query.max_price as string) || '')
const ordering = ref((route.query.ordering as string) || '-created_at')
const currentPage = ref(Number(route.query.page) || 1)
const pageSize = 12

const showFilters = ref(false)

const brands = ['Apple', 'Samsung', 'Xiaomi', 'Motorola', 'Honor', 'Oppo']

const sortOptions = [
  { value: '-created_at', label: 'Mas recientes' },
  { value: 'created_at', label: 'Mas antiguos' },
  { value: 'price', label: 'Menor precio' },
  { value: '-price', label: 'Mayor precio' },
  { value: 'name', label: 'Nombre A-Z' },
  { value: '-name', label: 'Nombre Z-A' },
]

const hasActiveFilters = computed(() =>
  search.value || selectedCategory.value || selectedBrand.value || minPrice.value || maxPrice.value
)

async function fetchProducts() {
  loading.value = true
  try {
    const filters: ProductFilters = {
      page: currentPage.value,
      page_size: pageSize,
      ordering: ordering.value,
    }
    if (search.value) filters.search = search.value
    if (selectedCategory.value) filters.category_id = selectedCategory.value
    if (selectedBrand.value) filters.brand = selectedBrand.value
    if (minPrice.value) filters.min_price = minPrice.value
    if (maxPrice.value) filters.max_price = maxPrice.value

    const data = await productsApi.list(filters)
    products.value = data.items
    total.value = data.total
    pages.value = data.pages
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    categories.value = await categoriesApi.list()
  } catch {
    categories.value = []
  }
}

function applyFilters() {
  currentPage.value = 1
  updateUrl()
  fetchProducts()
}

function clearFilters() {
  search.value = ''
  selectedCategory.value = undefined
  selectedBrand.value = ''
  minPrice.value = ''
  maxPrice.value = ''
  ordering.value = '-created_at'
  currentPage.value = 1
  updateUrl()
  fetchProducts()
}

function updateUrl() {
  const query: Record<string, string> = {}
  if (search.value) query.search = search.value
  if (selectedCategory.value) query.category_id = String(selectedCategory.value)
  if (selectedBrand.value) query.brand = selectedBrand.value
  if (minPrice.value) query.min_price = minPrice.value
  if (maxPrice.value) query.max_price = maxPrice.value
  if (ordering.value !== '-created_at') query.ordering = ordering.value
  if (currentPage.value > 1) query.page = String(currentPage.value)
  router.replace({ query })
}

function goToPage(page: number) {
  currentPage.value = page
  updateUrl()
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

let searchTimeout: ReturnType<typeof setTimeout>
function onSearchInput() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(applyFilters, 400)
}

onMounted(() => {
  fetchCategories()
  fetchProducts()
})

watch(ordering, applyFilters)
</script>

<template>
  <section class="py-10 sm:py-16 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="font-black text-3xl sm:text-4xl uppercase">Tienda</h1>
          <p class="text-brutal-black/60 font-semibold mt-1">{{ total }} productos encontrados</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="relative flex-1 sm:w-64">
            <Search :size="16" :stroke-width="2.5" class="absolute left-3 top-1/2 -translate-y-1/2 text-brutal-black/40" />
            <input
              v-model="search"
              type="text"
              placeholder="Buscar productos..."
              class="w-full pl-10 pr-4 py-2.5 brutal-border bg-brutal-white font-semibold text-sm focus:outline-none focus:bg-brutal-yellow/20 transition-colors"
              @input="onSearchInput"
            />
          </div>
          <button
            class="lg:hidden brutal-border p-2.5 bg-brutal-white hover:bg-brutal-yellow transition-colors"
            @click="showFilters = !showFilters"
          >
            <SlidersHorizontal :size="18" :stroke-width="2.5" />
          </button>
        </div>
      </div>

      <div class="flex gap-8">
        <aside :class="['w-64 shrink-0 space-y-6', showFilters ? 'block' : 'hidden lg:block']">
          <div v-if="showFilters" class="lg:hidden flex items-center justify-between mb-2">
            <span class="font-black uppercase">Filtros</span>
            <button @click="showFilters = false"><X :size="20" /></button>
          </div>

          <div class="brutal-card p-4">
            <h3 class="font-black text-sm uppercase mb-3">Categoria</h3>
            <div class="space-y-2">
              <label class="flex items-center gap-2 cursor-pointer group">
                <input type="radio" :checked="!selectedCategory" class="accent-brutal-yellow" @change="selectedCategory = undefined; applyFilters()" />
                <span class="text-sm font-semibold group-hover:text-brutal-black/70">Todas</span>
              </label>
              <label v-for="cat in categories" :key="cat.id" class="flex items-center gap-2 cursor-pointer group">
                <input type="radio" :value="cat.id" :checked="selectedCategory === cat.id" class="accent-brutal-yellow" @change="selectedCategory = cat.id; applyFilters()" />
                <span class="text-sm font-semibold group-hover:text-brutal-black/70">{{ cat.name }}</span>
              </label>
            </div>
          </div>

          <div class="brutal-card p-4">
            <h3 class="font-black text-sm uppercase mb-3">Marca</h3>
            <div class="space-y-2">
              <label class="flex items-center gap-2 cursor-pointer group">
                <input type="radio" :checked="!selectedBrand" class="accent-brutal-yellow" @change="selectedBrand = ''; applyFilters()" />
                <span class="text-sm font-semibold group-hover:text-brutal-black/70">Todas</span>
              </label>
              <label v-for="brand in brands" :key="brand" class="flex items-center gap-2 cursor-pointer group">
                <input type="radio" :value="brand" :checked="selectedBrand === brand" class="accent-brutal-yellow" @change="selectedBrand = brand; applyFilters()" />
                <span class="text-sm font-semibold group-hover:text-brutal-black/70">{{ brand }}</span>
              </label>
            </div>
          </div>

          <div class="brutal-card p-4">
            <h3 class="font-black text-sm uppercase mb-3">Precio</h3>
            <div class="flex items-center gap-2">
              <input v-model="minPrice" type="number" placeholder="Min" min="0" class="w-full px-3 py-2 brutal-border bg-brutal-white text-sm font-semibold focus:outline-none" @change="applyFilters" />
              <span class="font-bold text-brutal-black/40">-</span>
              <input v-model="maxPrice" type="number" placeholder="Max" min="0" class="w-full px-3 py-2 brutal-border bg-brutal-white text-sm font-semibold focus:outline-none" @change="applyFilters" />
            </div>
          </div>

          <button v-if="hasActiveFilters" class="w-full brutal-button bg-brutal-black text-brutal-white py-2.5 text-sm uppercase tracking-wide" @click="clearFilters">
            Limpiar filtros
          </button>
        </aside>

        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-2">
              <label class="text-sm font-bold">Ordenar:</label>
              <div class="relative">
                <select v-model="ordering" class="appearance-none brutal-border bg-brutal-white px-4 py-2 pr-8 text-sm font-bold cursor-pointer focus:outline-none">
                  <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
                <ChevronDown :size="14" class="absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            </div>
          </div>

          <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            <div v-for="i in 6" :key="i" class="brutal-card p-0 overflow-hidden">
              <div class="skeleton aspect-square"></div>
              <div class="p-5 space-y-3">
                <div class="skeleton h-6 w-3/4"></div>
                <div class="skeleton h-4 w-full"></div>
                <div class="skeleton h-12 w-full"></div>
              </div>
            </div>
          </div>

          <div v-else-if="products.length === 0" class="brutal-card p-12 text-center">
            <p class="font-black text-2xl uppercase mb-2">Sin resultados</p>
            <p class="text-brutal-black/60 mb-6">No se encontraron productos con esos filtros.</p>
            <button class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 uppercase tracking-wide" @click="clearFilters">
              Limpiar filtros
            </button>
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            <ProductCard v-for="(product, index) in products" :key="product.id" :product="product" :visible="true" :index="index" />
          </div>

          <div v-if="pages > 1" class="flex justify-center gap-2 mt-10">
            <button :disabled="currentPage <= 1" class="brutal-border bg-brutal-white px-4 py-2 font-bold text-sm uppercase disabled:opacity-40 hover:bg-brutal-yellow transition-colors" @click="goToPage(currentPage - 1)">
              Anterior
            </button>
            <button
              v-for="p in Math.min(pages, 5)"
              :key="p"
              :class="['brutal-border px-4 py-2 font-bold text-sm uppercase transition-colors', p === currentPage ? 'bg-brutal-yellow' : 'bg-brutal-white hover:bg-brutal-gray']"
              @click="goToPage(p)"
            >
              {{ p }}
            </button>
            <button :disabled="currentPage >= pages" class="brutal-border bg-brutal-white px-4 py-2 font-bold text-sm uppercase disabled:opacity-40 hover:bg-brutal-yellow transition-colors" @click="goToPage(currentPage + 1)">
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
