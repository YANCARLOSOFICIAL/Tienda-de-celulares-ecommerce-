<script setup lang="ts">
import { computed, ref } from 'vue'
import { ChevronDown, Cpu, Smartphone, Battery, HardDrive } from '@lucide/vue'
import type { Product } from '@/api/products'

const props = defineProps<{
  product: Product
}>()

interface SpecSection {
  title: string
  icon: any
  specs: { label: string; value: string }[]
}

const expandedSections = ref<Set<string>>(new Set(['general']))

const sections = computed<SpecSection[]>(() => {
  const general: { label: string; value: string }[] = []
  const hardware: { label: string; value: string }[] = []
  const battery: { label: string; value: string }[] = []
  const storage: { label: string; value: string }[] = []

  if (props.product.brand) general.push({ label: 'Marca', value: props.product.brand })
  if (props.product.model) general.push({ label: 'Modelo', value: props.product.model })
  if (props.product.category?.name) general.push({ label: 'Categoría', value: props.product.category.name })
  if (props.product.description) {
    const desc = props.product.description
    const ramMatch = desc.match(/(\d+\s*GB\s*RAM)/i)
    const storageMatch = desc.match(/(\d+\s*GB\s*(?:de\s+)?(?:almacenamiento|storage|memoria))/i)
    const batteryMatch = desc.match(/(\d+\s*mAh)/i)
    const screenMatch = desc.match(/(\d+\.?\d*\s*(?:pulgadas|inches|"))/i)
    const processorMatch = desc.match(/((?:Snapdragon|Exynos|A\d+|Dimensity|Helio)\s*\w+)/i)

    if (processorMatch) hardware.push({ label: 'Procesador', value: processorMatch[1] })
    if (screenMatch) hardware.push({ label: 'Pantalla', value: screenMatch[1] })
    if (ramMatch) hardware.push({ label: 'RAM', value: ramMatch[1] })
    if (batteryMatch) battery.push({ label: 'Batería', value: batteryMatch[1] })
    if (storageMatch) storage.push({ label: 'Almacenamiento', value: storageMatch[1] })
  }

  const result: SpecSection[] = []
  if (general.length > 0) result.push({ title: 'General', icon: Smartphone, specs: general })
  if (hardware.length > 0) result.push({ title: 'Hardware', icon: Cpu, specs: hardware })
  if (storage.length > 0) result.push({ title: 'Almacenamiento', icon: HardDrive, specs: storage })
  if (battery.length > 0) result.push({ title: 'Batería', icon: Battery, specs: battery })

  return result
})

function toggleSection(title: string) {
  if (expandedSections.value.has(title)) {
    expandedSections.value.delete(title)
  } else {
    expandedSections.value.add(title)
  }
}
</script>

<template>
  <div v-if="sections.length > 0" class="space-y-2">
    <div
      v-for="section in sections"
      :key="section.title"
      class="bg-surface-dim border border-border rounded-2xl overflow-hidden"
    >
      <button
        class="w-full flex items-center justify-between p-4 hover:bg-accent/5 transition-colors"
        @click="toggleSection(section.title)"
      >
        <div class="flex items-center gap-3">
          <component :is="section.icon" :size="18" :stroke-width="1.75" class="text-blue-500" />
          <span class="font-semibold text-sm text-text">{{ section.title }}</span>
        </div>
        <ChevronDown
          :size="16"
          :stroke-width="2"
          class="text-text-tertiary transition-transform duration-200"
          :class="{ 'rotate-180': expandedSections.has(section.title) }"
        />
      </button>
      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="opacity-0 max-h-0"
        enter-to-class="opacity-100 max-h-96"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="opacity-100 max-h-96"
        leave-to-class="opacity-0 max-h-0"
      >
        <div
          v-show="expandedSections.has(section.title)"
          class="overflow-hidden"
        >
          <div class="px-4 pb-4 grid grid-cols-2 gap-4 border-t border-border/50">
            <div
              v-for="spec in section.specs"
              :key="spec.label"
              class="space-y-1 p-2 rounded-lg hover:bg-accent/5 transition-colors"
            >
              <span class="text-xs uppercase tracking-wide text-text-secondary">{{ spec.label }}</span>
              <p class="font-semibold text-sm text-text">{{ spec.value }}</p>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>
