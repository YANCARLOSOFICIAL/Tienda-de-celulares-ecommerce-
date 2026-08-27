<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Product } from '@/api/products'

const props = defineProps<{
  product: Product
}>()

const emit = defineEmits<{
  (e: 'select-variant', variant: { storage?: string; color?: string }): void
}>()

const selectedStorage = ref<string | null>(null)
const selectedColor = ref<string | null>(null)

const storages = computed(() => {
  const matches = props.product.description?.match(/(\d+)\s*GB/gi) || []
  return [...new Set(matches.map(m => m.toUpperCase()))]
})

const colors = computed(() => {
  const colorMap: Record<string, string> = {
    'negro': '#000000',
    'black': '#000000',
    'blanco': '#FFFFFF',
    'white': '#FFFFFF',
    'azul': '#007AFF',
    'blue': '#007AFF',
    'verde': '#34C759',
    'green': '#34C759',
    'rojo': '#FF3B30',
    'red': '#FF3B30',
    'dorado': '#FFD60A',
    'gold': '#FFD60A',
    'plata': '#8E8E93',
    'silver': '#8E8E93',
    'purpura': '#AF52DE',
    'purple': '#AF52DE',
  }

  const colorNames = Object.keys(colorMap)
  const found = colorNames.filter(name =>
    props.product.description?.toLowerCase().includes(name) ||
    props.product.name.toLowerCase().includes(name)
  )

  if (found.length === 0) {
    return [
      { name: 'Negro', hex: '#000000' },
      { name: 'Blanco', hex: '#FFFFFF' },
    ]
  }

  return found.map(name => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    hex: colorMap[name],
  }))
})

function selectStorage(storage: string) {
  selectedStorage.value = storage
  emitVariant()
}

function selectColor(color: string) {
  selectedColor.value = color
  emitVariant()
}

function emitVariant() {
  emit('select-variant', {
    storage: selectedStorage.value || undefined,
    color: selectedColor.value || undefined,
  })
}
</script>

<template>
  <div class="space-y-4">
    <div v-if="storages.length > 0">
      <label class="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
        Almacenamiento
      </label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="storage in storages"
          :key="storage"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-all"
          :class="selectedStorage === storage
            ? 'bg-accent text-black'
            : 'bg-surface-dim border border-border text-text-secondary hover:border-white/10 hover:text-white'"
          @click="selectStorage(storage)"
        >
          {{ storage }}
        </button>
      </div>
    </div>

    <div v-if="colors.length > 0">
      <label class="text-xs font-semibold text-text-secondary uppercase tracking-wider block mb-2">
        Color
      </label>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="color in colors"
          :key="color.name"
          class="w-8 h-8 rounded-full border-2 transition-all flex items-center justify-center"
          :class="selectedColor === color.name
            ? 'border-blue-500 scale-110'
            : 'border-border hover:border-white/10'"
          :title="color.name"
          @click="selectColor(color.name)"
        >
          <div
            class="w-5 h-5 rounded-full"
            :style="{ backgroundColor: color.hex }"
          ></div>
        </button>
      </div>
      <p v-if="selectedColor" class="text-xs text-text-secondary mt-1.5">{{ selectedColor }}</p>
    </div>
  </div>
</template>
