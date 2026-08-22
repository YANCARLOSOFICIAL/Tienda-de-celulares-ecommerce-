<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, X, ArrowRight } from '@lucide/vue'
import { productsApi, type Product } from '../api/products'

const router = useRouter()
const query = ref('')
const results = ref<Product[]>([])
const isOpen = ref(false)
const isLoading = ref(false)
const inputRef = ref<HTMLInputElement | null>(null)
const recentSearches = ref<string[]>([])

const MAX_RECENT = 5

onMounted(() => {
  const saved = localStorage.getItem('tiendacell_recent_searches')
  if (saved) {
    try {
      recentSearches.value = JSON.parse(saved)
    } catch {
      recentSearches.value = []
    }
  }
})

function saveRecentSearch(term: string) {
  if (!term.trim()) return
  recentSearches.value = [term, ...recentSearches.value.filter(s => s !== term)].slice(0, MAX_RECENT)
  localStorage.setItem('tiendacell_recent_searches', JSON.stringify(recentSearches.value))
}

function removeRecentSearch(term: string) {
  recentSearches.value = recentSearches.value.filter(s => s !== term)
  localStorage.setItem('tiendacell_recent_searches', JSON.stringify(recentSearches.value))
}

let debounceTimer: ReturnType<typeof setTimeout>

watch(query, (val) => {
  clearTimeout(debounceTimer)
  if (!val.trim()) {
    results.value = []
    isLoading.value = false
    return
  }
  isLoading.value = true
  debounceTimer = setTimeout(async () => {
    try {
      const page = await productsApi.list({ search: val.trim(), page_size: 6 })
      results.value = page.items
    } catch {
      results.value = []
    } finally {
      isLoading.value = false
    }
  }, 250)
})

function selectProduct(product: Product) {
  saveRecentSearch(query.value.trim())
  query.value = ''
  results.value = []
  isOpen.value = false
  router.push(`/products/${product.id}`)
}

function searchAll() {
  if (!query.value.trim()) return
  saveRecentSearch(query.value.trim())
  isOpen.value = false
  router.push({ path: '/shop', query: { search: query.value.trim() } })
  query.value = ''
  results.value = []
}

function selectRecent(term: string) {
  query.value = term
  inputRef.value?.focus()
}

function close() {
  isOpen.value = false
  query.value = ''
  results.value = []
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}

function handleClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.predictive-search')) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})

function formatPrice(price: string): string {
  return Number(price).toLocaleString('es-MX')
}
</script>

<template>
  <div class="predictive-search relative">
    <div
      class="flex items-center gap-2 bg-surface-dim border border-border rounded-xl px-3 py-2 transition-all focus-within:border-blue-500"
      :class="{ 'border-blue-500': isOpen }"
    >
      <Search :size="16" :stroke-width="1.75" class="text-text-tertiary shrink-0" />
      <input
        ref="inputRef"
        v-model="query"
        type="text"
        placeholder="Buscar celulares, accesorios..."
        class="flex-1 bg-transparent text-sm text-white outline-none placeholder:text-text-tertiary"
        @focus="isOpen = true"
        @keydown.enter="searchAll"
      />
      <button
        v-if="query"
        class="p-0.5 text-text-tertiary hover:text-white transition-colors"
        @click="query = ''; results = []"
      >
        <X :size="14" :stroke-width="2" />
      </button>
    </div>

    <Transition
      enter-active-class="transition ease-out duration-150"
      enter-from-class="opacity-0 -translate-y-1 scale-[0.98]"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 -translate-y-1 scale-[0.98]"
    >
      <div
        v-if="isOpen && (query.trim() || recentSearches.length > 0)"
        class="absolute top-full left-0 right-0 mt-2 bg-surface-dim border border-border rounded-2xl shadow-2xl shadow-black/50 overflow-hidden z-50"
      >
        <div v-if="isLoading" class="p-4 space-y-3">
          <div v-for="i in 3" :key="i" class="flex items-center gap-3">
            <div class="skeleton w-10 h-10 rounded-lg shrink-0"></div>
            <div class="flex-1 space-y-1.5">
              <div class="skeleton h-3.5 w-3/4 rounded"></div>
              <div class="skeleton h-3 w-1/4 rounded"></div>
            </div>
          </div>
        </div>

        <div v-else-if="query.trim() && results.length > 0">
          <div class="p-2">
            <div
              v-for="product in results"
              :key="product.id"
              class="flex items-center gap-3 p-2 rounded-xl cursor-pointer hover:bg-surface-hover transition-colors"
              @click="selectProduct(product)"
            >
              <img
                :src="product.image || 'https://placehold.co/80x80/1C1C1E/8E8E93?text=IMG&font=inter'"
                :alt="product.name"
                class="w-10 h-10 rounded-lg object-cover bg-surface shrink-0"
              />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-white truncate">{{ product.name }}</p>
                <p class="text-xs text-text-secondary">{{ product.brand }} · ${{ formatPrice(product.price) }}</p>
              </div>
              <ArrowRight :size="14" class="text-text-tertiary shrink-0" />
            </div>
          </div>
          <button
            class="w-full px-4 py-2.5 text-sm font-medium text-blue-500 hover:bg-surface-hover border-t border-border transition-colors flex items-center justify-center gap-2"
            @click="searchAll"
          >
            Ver todos los resultados
            <ArrowRight :size="14" />
          </button>
        </div>

        <div v-else-if="query.trim() && results.length === 0" class="p-6 text-center">
          <p class="text-sm text-text-secondary">No se encontraron resultados</p>
          <p class="text-xs text-text-tertiary mt-1">Intenta con otro término</p>
        </div>

        <div v-else-if="recentSearches.length > 0" class="p-2">
          <p class="px-3 py-1.5 text-xs font-semibold text-text-tertiary uppercase tracking-wider">Búsquedas recientes</p>
          <div
            v-for="term in recentSearches"
            :key="term"
            class="flex items-center justify-between px-3 py-2 rounded-xl cursor-pointer hover:bg-surface-hover transition-colors group"
            @click="selectRecent(term)"
          >
            <span class="text-sm text-text-secondary group-hover:text-white transition-colors">{{ term }}</span>
            <button
              class="p-0.5 text-text-tertiary hover:text-danger opacity-0 group-hover:opacity-100 transition-all"
              @click.stop="removeRecentSearch(term)"
            >
              <X :size="12" :stroke-width="2" />
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
