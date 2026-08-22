<script setup lang="ts">
import { computed } from 'vue'
import type { Product } from '../api/products'

const props = defineProps<{
  product: Product
}>()

interface Spec {
  label: string
  value: string
}

const specs = computed<Spec[]>(() => {
  const items: Spec[] = []
  if (props.product.brand) items.push({ label: 'Marca', value: props.product.brand })
  if (props.product.model) items.push({ label: 'Modelo', value: props.product.model })
  if (props.product.category?.name) items.push({ label: 'Categoría', value: props.product.category.name })
  return items
})
</script>

<template>
  <div v-if="specs.length > 0" class="brutal-card p-5 sm:p-6">
    <h3 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
      <span class="bg-brutal-yellow p-1.5 brutal-border text-xs">📋</span>
      Especificaciones
    </h3>
    <div class="space-y-0">
      <div
        v-for="(spec, index) in specs"
        :key="spec.label"
        class="flex justify-between items-center py-3 border-b-2 border-brutal-black/10 last:border-b-0"
      >
        <span class="text-sm font-semibold text-brutal-black/60">{{ spec.label }}</span>
        <span class="font-bold text-sm text-right">{{ spec.value }}</span>
      </div>
    </div>
  </div>
</template>
