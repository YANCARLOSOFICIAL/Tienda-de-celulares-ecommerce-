<script setup lang="ts">
import { useRouter } from 'vue-router'
import { X, ArrowRight, Scale } from '@lucide/vue'
import { useCompareStore } from '../stores/compare'
import { formatPrice } from '../api/products'

const router = useRouter()
const compareStore = useCompareStore()

function goToCompare() {
  if (compareStore.count < 2) return
  router.push('/compare')
}
</script>

<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="translate-y-full opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-full opacity-0"
  >
    <div
      v-if="compareStore.count > 0"
      class="fixed bottom-0 left-0 right-0 z-50 bg-surface-dim/95 backdrop-blur-xl border-t border-accent/30 shadow-[0_-4px_20px_rgba(0,212,255,0.1)]"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-3 overflow-x-auto no-scrollbar">
            <div class="flex items-center gap-2 shrink-0">
              <Scale :size="18" :stroke-width="2" class="text-accent" />
              <span class="text-sm font-semibold text-text">
                Comparar ({{ compareStore.count }}/3)
              </span>
            </div>
            <div class="flex gap-2">
              <div
                v-for="product in compareStore.items"
                :key="product.id"
                class="flex items-center gap-2 bg-surface border border-border rounded-xl px-3 py-1.5 shrink-0"
              >
                <img
                  :src="product.image || 'https://placehold.co/40x40/1C1C1E/8E8E93?text=P&font=inter'"
                  :alt="product.name"
                  class="w-8 h-8 rounded-lg object-cover"
                />
                <div class="max-w-[120px]">
                  <p class="text-xs font-medium text-text truncate">{{ product.name }}</p>
                  <p class="text-[10px] text-accent">${{ formatPrice(product.price) }}</p>
                </div>
                <button
                  class="p-0.5 text-text-tertiary hover:text-danger transition-colors shrink-0"
                  @click="compareStore.remove(product.id)"
                >
                  <X :size="12" :stroke-width="2" />
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <button
              class="btn-ghost text-xs"
              @click="compareStore.clear()"
            >
              Limpiar
            </button>
            <button
              class="btn-primary text-xs px-4 py-2 flex items-center gap-1.5 disabled:opacity-40"
              :disabled="compareStore.count < 2"
              @click="goToCompare"
            >
              Comparar
              <ArrowRight :size="14" :stroke-width="2" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>