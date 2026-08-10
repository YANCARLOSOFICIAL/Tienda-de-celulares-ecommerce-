<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useProductsStore } from '../stores/products'
import ProductCard from './ProductCard.vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const store = useProductsStore()
const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)
const error = ref<string | null>(null)

onMounted(() => {
  try {
    store.fetchProducts()
  } catch (e) {
    error.value = 'Ocurrió un error al cargar los productos.'
  }
})

const displayedProducts = computed(() => store.products)
</script>

<template>
  <section
    id="productos"
    ref="sectionRef"
    class="py-16 sm:py-20 lg:py-28 bg-brutal-white"
    aria-labelledby="productos-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-4">
          CATÁLOGO
        </span>
        <h2 id="productos-title" class="section-title text-brutal-black mb-4">
          Productos Destacados
        </h2>
        <p class="section-subtitle">
          Los mejores smartphones con precios exclusivos. Aprovecha nuestras ofertas por tiempo limitado.
        </p>
      </div>

      <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
        <div v-for="i in 6" :key="i" class="brutal-border p-0 overflow-hidden">
          <div class="skeleton aspect-square"></div>
          <div class="p-5 space-y-3">
            <div class="skeleton h-6 w-3/4"></div>
            <div class="skeleton h-4 w-full"></div>
            <div class="skeleton h-4 w-1/2"></div>
            <div class="skeleton h-12 w-full"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-12">
        <p class="font-bold text-lg text-brutal-black">{{ error }}</p>
        <button
          class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 mt-4"
          @click="store.fetchProducts()"
        >
          Reintentar
        </button>
      </div>

      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8"
      >
        <ProductCard
          v-for="(product, index) in displayedProducts"
          :key="product.id"
          :product="product"
          :visible="isVisible"
          :index="index"
        />
      </div>
    </div>
  </section>
</template>
