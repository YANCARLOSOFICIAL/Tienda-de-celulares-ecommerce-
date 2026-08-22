<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { productsApi, type Product, type ProductPage } from '../api/products'
import ProductCard from './ProductCard.vue'

const props = defineProps<{
  categoryId: number | null
  currentProductId: number
}>()

const products = ref<Product[]>([])
const loading = ref(false)

async function fetchRelated() {
  if (!props.categoryId) return
  loading.value = true
  try {
    const data: ProductPage = await productsApi.list({
      category_id: props.categoryId,
      page_size: 4,
    })
    products.value = data.items.filter((p) => p.id !== props.currentProductId).slice(0, 3)
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchRelated)
watch(() => props.categoryId, fetchRelated)
</script>

<template>
  <section v-if="products.length > 0 || loading" class="py-12 sm:py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8 sm:mb-10">
        <h2 class="section-title text-text">También te puede interesar</h2>
      </div>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
        <div v-for="i in 3" :key="i" class="bg-surface rounded-2xl overflow-hidden">
          <div class="skeleton aspect-square rounded-none"></div>
          <div class="p-5 space-y-3">
            <div class="skeleton h-5 w-3/4 rounded-lg"></div>
            <div class="skeleton h-4 w-full rounded-lg"></div>
            <div class="skeleton h-10 w-full rounded-lg"></div>
          </div>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
        <ProductCard
          v-for="(product, index) in products"
          :key="product.id"
          :product="product"
          :visible="true"
          :index="index"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
:deep(.bento-card-static) {
  border: 1px solid var(--color-border);
  transition: border-color 0.3s, box-shadow 0.3s;
}
:deep(.bento-card-static:hover) {
  border-color: var(--color-accent);
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
}
</style>
