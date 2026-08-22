<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ChevronLeft, ChevronRight, ZoomIn } from '@lucide/vue'

const props = defineProps<{
  image: string | null
  name: string
}>()

const mainImage = ref(props.image || 'https://placehold.co/800x800/111111/FFD60A?text=Sin+imagen&font=inter')
const lightboxOpen = ref(false)

watch(() => props.image, (newImage) => {
  mainImage.value = newImage || 'https://placehold.co/800x800/111111/FFD60A?text=Sin+imagen&font=inter'
})

function openLightbox() {
  lightboxOpen.value = true
}

function closeLightbox() {
  lightboxOpen.value = false
}
</script>

<template>
  <div class="space-y-4">
    <div
      class="relative brutal-card overflow-hidden bg-brutal-gray cursor-zoom-in group"
      @click="openLightbox"
    >
      <img
        :src="mainImage"
        :alt="name"
        class="w-full aspect-square object-cover transition-transform duration-500 group-hover:scale-105"
      />
      <div class="absolute top-3 right-3 bg-brutal-black text-brutal-white p-2 brutal-border opacity-80 group-hover:opacity-100 transition-opacity">
        <ZoomIn :size="20" :stroke-width="2.5" />
      </div>
    </div>

    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-200"
        leave-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-50 flex items-center justify-center bg-brutal-black/90 p-4"
          @click.self="closeLightbox"
        >
          <button
            class="absolute top-4 right-4 text-brutal-white bg-brutal-black/50 hover:bg-brutal-black p-2 brutal-border z-10"
            @click="closeLightbox"
          >
            ✕
          </button>
          <img
            :src="mainImage"
            :alt="name"
            class="max-w-full max-h-[90vh] object-contain brutal-border"
          />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
