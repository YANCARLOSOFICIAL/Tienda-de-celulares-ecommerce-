<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useProductsStore } from '@/stores/products'
import ProductCard from '@/components/product/ProductCard.vue'
import { useIntersectionObserver } from '@/composables/useIntersectionObserver'

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
    class="section-clean bg-surface"
    aria-labelledby="productos-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="badge badge-accent mb-4">Catálogo</span>
        <h2 id="productos-title" class="section-title mb-4">
          Productos Destacados
        </h2>
        <p class="section-subtitle mx-auto">
          Los mejores smartphones con precios exclusivos. Aprovecha nuestras ofertas por tiempo limitado.
        </p>
      </div>

      <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bento-card-static overflow-hidden bg-surface-dim">
          <div class="skeleton aspect-square rounded-none bg-surface-dim"></div>
          <div class="p-5 space-y-3">
            <div class="skeleton h-5 w-3/4"></div>
            <div class="skeleton h-3.5 w-full"></div>
            <div class="skeleton h-3.5 w-1/2"></div>
            <div class="skeleton h-10 w-full"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="text-center py-16">
        <p class="text-text-secondary mb-4">{{ error }}</p>
        <button class="btn-primary" @click="store.fetchProducts()">
          Reintentar
        </button>
      </div>

      <div
        v-else
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
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
