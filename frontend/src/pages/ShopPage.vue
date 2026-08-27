<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, SlidersHorizontal, X, ChevronDown } from '@lucide/vue'

import { productsApi, type Product, type ProductFilters } from '@/api/products'
import { categoriesApi, type Category } from '@/api/categories'
import ProductCard from '@/components/product/ProductCard.vue'

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

const activeFilters = computed(() => {
  const filters: { key: string; label: string; clear: () => void }[] = []
  if (search.value) {
    filters.push({ key: 'search', label: `"${search.value}"`, clear: () => { search.value = '' } })
  }
  if (selectedCategory.value) {
    const cat = categories.value.find(c => c.id === selectedCategory.value)
    filters.push({ key: 'category', label: cat?.name || 'Categoria', clear: () => { selectedCategory.value = undefined } })
  }
  if (selectedBrand.value) {
    filters.push({ key: 'brand', label: selectedBrand.value, clear: () => { selectedBrand.value = '' } })
  }
  if (minPrice.value) {
    filters.push({ key: 'min_price', label: `Min $${minPrice.value}`, clear: () => { minPrice.value = '' } })
  }
  if (maxPrice.value) {
    filters.push({ key: 'max_price', label: `Max $${maxPrice.value}`, clear: () => { maxPrice.value = '' } })
  }
  return filters
})

const hasActiveFilters = computed(() => activeFilters.value.length > 0)

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

function removeFilter(filter: { key: string; clear: () => void }) {
  filter.clear()
  applyFilters()
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
  <section class="section-clean min-h-[70vh]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-3xl sm:text-4xl font-bold text-text tracking-tight" style="font-family: var(--font-family-serif);">Tienda</h1>
          <p class="text-text-secondary text-sm mt-1">{{ total }} productos encontrados</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="relative flex-1 sm:w-64">
            <Search :size="16" class="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" />
            <input
              v-model="search"
              type="text"
              placeholder="Buscar productos..."
              class="input-minimal w-full pl-10 pr-4"
              @input="onSearchInput"
            />
          </div>
          <button
            class="lg:hidden btn-secondary p-2.5 rounded-xl border-border hover:border-white/10"
            @click="showFilters = !showFilters"
          >
            <SlidersHorizontal :size="18" />
          </button>
        </div>
      </div>

      <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mb-6">
        <span
          v-for="filter in activeFilters"
          :key="filter.key"
          class="badge badge-accent flex items-center gap-1.5 pr-1.5"
        >
          {{ filter.label }}
          <button
            class="w-5 h-5 flex items-center justify-center rounded-full hover:bg-accent/10 transition-colors"
            @click="removeFilter(filter)"
          >
            <X :size="12" />
          </button>
        </span>
        <button class="text-xs text-text-secondary hover:text-text transition-colors underline" @click="clearFilters">
          Limpiar todo
        </button>
      </div>

      <div class="flex gap-8">
        <aside :class="['w-[280px] shrink-0 space-y-5', showFilters ? 'block' : 'hidden lg:block']">
          <div v-if="showFilters" class="lg:hidden flex items-center justify-between mb-2">
            <span class="font-semibold text-text">Filtros</span>
            <button @click="showFilters = false" class="text-text-secondary hover:text-text transition-colors">
              <X :size="20" />
            </button>
          </div>

          <div class="bento-card p-5">
            <h3 class="text-sm font-semibold text-text mb-3" style="font-family: var(--font-family-serif);">Categoria</h3>
            <div class="space-y-2.5">
              <label class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="radio"
                  :checked="!selectedCategory"
                  class="accent-blue-500 w-4 h-4"
                  @change="selectedCategory = undefined; applyFilters()"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">Todas</span>
              </label>
              <label v-for="cat in categories" :key="cat.id" class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="radio"
                  :value="cat.id"
                  :checked="selectedCategory === cat.id"
                  class="accent-blue-500 w-4 h-4"
                  @change="selectedCategory = cat.id; applyFilters()"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">{{ cat.name }}</span>
              </label>
            </div>
          </div>

          <div class="bento-card p-5">
            <h3 class="text-sm font-semibold text-text mb-3" style="font-family: var(--font-family-serif);">Marca</h3>
            <div class="space-y-2.5">
              <label class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="radio"
                  :checked="!selectedBrand"
                  class="accent-blue-500 w-4 h-4"
                  @change="selectedBrand = ''; applyFilters()"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">Todas</span>
              </label>
              <label v-for="brand in brands" :key="brand" class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="radio"
                  :value="brand"
                  :checked="selectedBrand === brand"
                  class="accent-blue-500 w-4 h-4"
                  @change="selectedBrand = brand; applyFilters()"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">{{ brand }}</span>
              </label>
            </div>
          </div>

          <div class="bento-card p-5">
            <h3 class="text-sm font-semibold text-text mb-3" style="font-family: var(--font-family-serif);">Precio</h3>
            <div class="flex items-center gap-2">
              <input
                v-model="minPrice"
                type="number"
                placeholder="Min"
                min="0"
                class="input-minimal w-full"
                @change="applyFilters"
              />
              <span class="text-text-secondary text-sm">-</span>
              <input
                v-model="maxPrice"
                type="number"
                placeholder="Max"
                min="0"
                class="input-minimal w-full"
                @change="applyFilters"
              />
            </div>
          </div>

          <button
            v-if="hasActiveFilters"
            class="btn-ghost w-full py-2.5 text-sm font-medium text-text-secondary hover:text-text transition-colors"
            @click="clearFilters"
          >
            Limpiar filtros
          </button>
        </aside>

        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-2">
              <label class="text-sm text-text-secondary">Ordenar:</label>
              <div class="relative">
                <select
                  v-model="ordering"
                  class="appearance-none bg-surface-dim border border-border rounded-xl px-3 py-1.5 text-sm font-semibold text-text cursor-pointer focus:outline-none focus:border-gold focus:ring-1 focus:ring-gold/30 transition-colors pr-6"
                >
                  <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                </select>
                <ChevronDown :size="14" class="absolute right-0 top-1/2 -translate-y-1/2 pointer-events-none text-text-secondary" />
              </div>
            </div>
          </div>

          <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="i in 6" :key="i" class="bento-card p-0 overflow-hidden">
              <div class="skeleton aspect-square rounded-none"></div>
              <div class="p-4 space-y-2.5">
                <div class="skeleton h-3 w-16"></div>
                <div class="skeleton h-5 w-3/4"></div>
                <div class="skeleton h-4 w-20"></div>
                <div class="skeleton h-10 w-full rounded-xl"></div>
              </div>
            </div>
          </div>

          <div v-else-if="products.length === 0" class="bento-card p-16 text-center">
            <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-surface-dim flex items-center justify-center">
              <Search :size="28" class="text-text-tertiary" />
            </div>
            <p class="font-semibold text-lg text-text mb-1">No se encontraron productos</p>
            <p class="text-text-tertiary text-sm mb-6">Intenta ajustar los filtros de busqueda.</p>
            <button class="btn-gold px-6 py-2.5 rounded-full text-sm font-semibold" @click="clearFilters">
              Limpiar filtros
            </button>
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <ProductCard v-for="product in products" :key="product.id" :product="product" />
          </div>

          <div v-if="pages > 1" class="flex justify-center items-center gap-1.5 mt-10">
            <button
              :disabled="currentPage <= 1"
              class="w-10 h-10 flex items-center justify-center rounded-xl text-sm font-medium text-text-secondary hover:text-text hover:bg-surface-dim transition-colors disabled:opacity-30 disabled:pointer-events-none"
              @click="goToPage(currentPage - 1)"
            >
              Anterior
            </button>
            <button
              v-for="p in Math.min(pages, 5)"
              :key="p"
              :class="[
                'w-10 h-10 flex items-center justify-center rounded-xl text-sm font-medium transition-colors',
                p === currentPage ? 'bg-gold text-[#0e0f12]' : 'text-text-secondary hover:text-text hover:bg-surface-dim'
              ]"
              @click="goToPage(p)"
            >
              {{ p }}
            </button>
            <button
              :disabled="currentPage >= pages"
              class="w-10 h-10 flex items-center justify-center rounded-xl text-sm font-medium text-text-secondary hover:text-text hover:bg-surface-dim transition-colors disabled:opacity-30 disabled:pointer-events-none"
              @click="goToPage(currentPage + 1)"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
