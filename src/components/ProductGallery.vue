<script setup lang="ts">
import { ref, watch } from 'vue'
import { ChevronLeft, ChevronRight, ZoomIn } from '@lucide/vue'

const props = defineProps<{
  image: string | null
  name: string
}>()

const mainImage = ref(props.image || 'https://placehold.co/800x800/FAFAFA/1D1D1F?text=Sin+imagen&font=inter')
const lightboxOpen = ref(false)

watch(() => props.image, (newImage) => {
  mainImage.value = newImage || 'https://placehold.co/800x800/FAFAFA/1D1D1F?text=Sin+imagen&font=inter'
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
      class="relative overflow-hidden bg-[#0a0a0f] border border-cyan-500/40 shadow-[0_0_15px_rgba(0,255,255,0.1)] rounded-2xl cursor-zoom-in group hover:border-cyan-400 hover:shadow-[0_0_25px_rgba(0,255,255,0.2)] transition-all duration-300"
      @click="openLightbox"
    >
      <img
        :src="mainImage"
        :alt="name"
        class="w-full aspect-square object-cover rounded-xl transition-transform duration-500 group-hover:scale-105"
      />
      <div class="absolute top-3 right-3 bg-[#0a0a0f]/80 backdrop-blur-sm text-cyan-400 p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
        <ZoomIn :size="20" :stroke-width="2" />
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
          class="fixed inset-0 z-50 flex items-center justify-center bg-[#0a0a0f]/90 backdrop-blur-md p-4"
          @click.self="closeLightbox"
        >
          <button
            class="absolute top-4 right-4 text-cyan-400 bg-[#0a0a0f]/60 hover:bg-cyan-500/20 hover:text-cyan-300 border border-cyan-500/30 hover:border-cyan-400 rounded-full p-3 transition-all z-10 hover:shadow-[0_0_15px_rgba(0,255,255,0.3)]"
            @click="closeLightbox"
          >
            ✕
          </button>
          <img
            :src="mainImage"
            :alt="name"
            class="max-w-full max-h-[90vh] object-contain rounded-2xl"
          />
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
