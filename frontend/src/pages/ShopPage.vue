<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, SlidersHorizontal, X } from '@lucide/vue'

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

function parseCsv(value: unknown): string[] {
  return typeof value === 'string' && value ? value.split(',').filter(Boolean) : []
}

const search = ref((route.query.search as string) || '')
const selectedCategories = ref<number[]>(parseCsv(route.query.category_id).map(Number).filter((n) => !Number.isNaN(n)))
const selectedBrands = ref<string[]>(parseCsv(route.query.brand))
const minPrice = ref((route.query.min_price as string) || '')
const maxPrice = ref((route.query.max_price as string) || '')
const ordering = ref((route.query.ordering as string) || '-created_at')
const currentPage = ref(Number(route.query.page) || 1)
const pageSize = 12

const showFilters = ref(false)

const brands = ref<string[]>([])

function toggleInArray<T>(arr: T[], value: T) {
  const i = arr.indexOf(value)
  if (i === -1) arr.push(value)
  else arr.splice(i, 1)
}

function toggleCategory(id: number) {
  toggleInArray(selectedCategories.value, id)
  applyFilters()
}

function toggleBrand(brand: string) {
  toggleInArray(selectedBrands.value, brand)
  applyFilters()
}

const sortOptions = [
  { value: '-created_at', label: 'Más recientes' },
  { value: 'created_at', label: 'Más antiguos' },
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
  for (const id of selectedCategories.value) {
    const cat = categories.value.find(c => c.id === id)
    filters.push({ key: `category-${id}`, label: cat?.name || 'Categoría', clear: () => toggleInArray(selectedCategories.value, id) })
  }
  for (const brand of selectedBrands.value) {
    filters.push({ key: `brand-${brand}`, label: brand, clear: () => toggleInArray(selectedBrands.value, brand) })
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
    if (selectedCategories.value.length) filters.category_id = [...selectedCategories.value]
    if (selectedBrands.value.length) filters.brand = [...selectedBrands.value]
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

async function fetchBrands() {
  try {
    brands.value = await productsApi.brands()
  } catch {
    brands.value = []
  }
}

function applyFilters() {
  currentPage.value = 1
  updateUrl()
  fetchProducts()
}

function clearFilters() {
  search.value = ''
  selectedCategories.value = []
  selectedBrands.value = []
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
  if (selectedCategories.value.length) query.category_id = selectedCategories.value.join(',')
  if (selectedBrands.value.length) query.brand = selectedBrands.value.join(',')
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
  fetchBrands()
  fetchProducts()
})

watch(ordering, applyFilters)
</script>

<template>
  <section class="page">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="page-header flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-8">
        <div>
          <p class="eyebrow">Catálogo</p>
          <h1 class="page-title">Tienda</h1>
          <p class="text-text-secondary text-sm mt-2">{{ total }} piezas disponibles</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="relative flex-1 sm:w-64">
            <Search :size="16" class="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary" />
            <input
              v-model="search"
              type="text"
              placeholder="Buscar productos..."
              class="maison-input w-full pl-10 pr-4"
              @input="onSearchInput"
            />
          </div>
          <button
            class="lg:hidden btn-outline p-3"
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
            class="w-5 h-5 flex items-center justify-center hover:bg-black/10 transition-colors"
            @click="removeFilter(filter)"
          >
            <X :size="12" />
          </button>
        </span>
        <button class="text-xs text-text-secondary hover:text-accent transition-colors uppercase tracking-widest" @click="clearFilters">
          Limpiar todo
        </button>
      </div>

      <div class="flex gap-8">
        <aside :class="['w-[280px] shrink-0 space-y-5', showFilters ? 'block' : 'hidden lg:block']">
          <div v-if="showFilters" class="lg:hidden flex items-center justify-between mb-2">
            <span class="eyebrow">Filtros</span>
            <button @click="showFilters = false" class="text-text-secondary hover:text-accent transition-colors">
              <X :size="20" />
            </button>
          </div>

          <div class="maison-panel p-5">
            <h3 class="filter-heading">Categoría</h3>
            <div class="space-y-2.5">
              <label v-for="cat in categories" :key="cat.id" class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="checkbox"
                  :value="cat.id"
                  :checked="selectedCategories.includes(cat.id)"
                  class="accent-[#f0c419] w-4 h-4"
                  @change="toggleCategory(cat.id)"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">{{ cat.name }}</span>
              </label>
            </div>
          </div>

          <div v-if="brands.length" class="maison-panel p-5">
            <h3 class="filter-heading">Marca</h3>
            <div class="space-y-2.5">
              <label v-for="brand in brands" :key="brand" class="flex items-center gap-2.5 cursor-pointer group">
                <input
                  type="checkbox"
                  :value="brand"
                  :checked="selectedBrands.includes(brand)"
                  class="accent-[#f0c419] w-4 h-4"
                  @change="toggleBrand(brand)"
                />
                <span class="text-sm text-text-secondary group-hover:text-text transition-colors">{{ brand }}</span>
              </label>
            </div>
          </div>

          <div class="maison-panel p-5">
            <h3 class="filter-heading">Precio</h3>
            <div class="flex items-center gap-2">
              <input
                v-model="minPrice"
                type="number"
                placeholder="Min"
                min="0"
                class="maison-input w-full"
                @change="applyFilters"
              />
              <span class="text-text-tertiary text-sm">—</span>
              <input
                v-model="maxPrice"
                type="number"
                placeholder="Max"
                min="0"
                class="maison-input w-full"
                @change="applyFilters"
              />
            </div>
          </div>

          <button
            v-if="hasActiveFilters"
            class="btn-ghost w-full justify-center"
            @click="clearFilters"
          >
            Limpiar filtros
          </button>
        </aside>

        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-border">
            <label class="eyebrow">Ordenar</label>
            <select v-model="ordering" class="maison-select w-auto min-w-[200px]">
              <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>

          <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="i in 6" :key="i" class="maison-card p-0 overflow-hidden">
              <div class="skeleton aspect-square"></div>
              <div class="p-4 space-y-2.5">
                <div class="skeleton h-3 w-16"></div>
                <div class="skeleton h-5 w-3/4"></div>
                <div class="skeleton h-4 w-20"></div>
                <div class="skeleton h-10 w-full"></div>
              </div>
            </div>
          </div>

          <div v-else-if="products.length === 0" class="maison-panel p-16 text-center">
            <div class="w-16 h-16 mx-auto mb-5 border border-border flex items-center justify-center">
              <Search :size="26" class="text-text-tertiary" />
            </div>
            <p class="text-display text-xl mb-2">No se encontraron productos</p>
            <p class="text-text-tertiary text-sm mb-7">Intenta ajustar los filtros de búsqueda.</p>
            <button class="btn-fill" @click="clearFilters">
              Limpiar filtros
            </button>
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <ProductCard v-for="product in products" :key="product.id" :product="product" />
          </div>

          <div v-if="pages > 1" class="flex justify-center items-center gap-1.5 mt-10">
            <button
              :disabled="currentPage <= 1"
              class="page-btn"
              @click="goToPage(currentPage - 1)"
            >
              Anterior
            </button>
            <button
              v-for="p in Math.min(pages, 5)"
              :key="p"
              :class="['page-btn', p === currentPage ? 'page-btn-active' : '']"
              @click="goToPage(p)"
            >
              {{ p }}
            </button>
            <button
              :disabled="currentPage >= pages"
              class="page-btn"
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

<style scoped>
.filter-heading {
  font-family: var(--font-family-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 14px;
}

.page-btn {
  min-width: 40px;
  height: 40px;
  padding: 0 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--color-text-secondary);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 0;
  cursor: pointer;
  transition: all 0.25s ease;
}

.page-btn:hover:not(:disabled) {
  color: var(--color-accent);
  border-color: rgba(240, 196, 25, 0.4);
}

.page-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.page-btn-active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: #0a0906;
  font-weight: 700;
}
</style>
