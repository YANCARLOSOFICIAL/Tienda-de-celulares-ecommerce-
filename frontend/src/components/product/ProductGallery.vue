<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { ChevronLeft, ChevronRight, ZoomIn, X } from '@lucide/vue'

const props = defineProps<{
  image: string | null
  images?: string[]
  name: string
}>()

const PLACEHOLDER = 'https://placehold.co/800x800/15181e/86868B?text=Sin+imagen&font=inter'

/** Galería efectiva: usa `images`, cae a `[image]`, y si no hay nada, al placeholder. */
const gallery = computed(() => {
  const list = (props.images ?? []).filter(Boolean)
  if (list.length) return list
  return props.image ? [props.image] : [PLACEHOLDER]
})

const activeIndex = ref(0)
const lightboxOpen = ref(false)

watch(gallery, () => { activeIndex.value = 0 })

const activeImage = computed(() => gallery.value[activeIndex.value] ?? PLACEHOLDER)
const hasMultiple = computed(() => gallery.value.length > 1)

function select(i: number) {
  activeIndex.value = (i + gallery.value.length) % gallery.value.length
}
function next() { select(activeIndex.value + 1) }
function prev() { select(activeIndex.value - 1) }

function openLightbox() {
  lightboxOpen.value = true
  document.addEventListener('keydown', onKey)
}
function closeLightbox() {
  lightboxOpen.value = false
  document.removeEventListener('keydown', onKey)
}
function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape') closeLightbox()
  else if (e.key === 'ArrowRight') next()
  else if (e.key === 'ArrowLeft') prev()
}

onUnmounted(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <div class="space-y-3">
    <!-- Imagen principal -->
    <div
      class="relative overflow-hidden bg-surface-dim border border-border rounded-2xl cursor-zoom-in group"
      @click="openLightbox"
    >
      <img
        :src="activeImage"
        :alt="`${name} — imagen ${activeIndex + 1}`"
        class="w-full aspect-square object-contain transition-transform duration-500 group-hover:scale-105"
      />
      <div class="absolute top-3 right-3 bg-surface-dim/80 backdrop-blur-sm text-text-secondary p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
        <ZoomIn :size="20" :stroke-width="2" />
      </div>

      <template v-if="hasMultiple">
        <button
          class="absolute left-2 top-1/2 -translate-y-1/2 bg-surface-dim/80 backdrop-blur-sm text-text-secondary hover:text-text rounded-full p-2 transition-colors"
          aria-label="Imagen anterior"
          @click.stop="prev"
        >
          <ChevronLeft :size="18" :stroke-width="2" />
        </button>
        <button
          class="absolute right-2 top-1/2 -translate-y-1/2 bg-surface-dim/80 backdrop-blur-sm text-text-secondary hover:text-text rounded-full p-2 transition-colors"
          aria-label="Imagen siguiente"
          @click.stop="next"
        >
          <ChevronRight :size="18" :stroke-width="2" />
        </button>
      </template>
    </div>

    <!-- Miniaturas -->
    <div v-if="hasMultiple" class="flex gap-2 overflow-x-auto no-scrollbar">
      <button
        v-for="(img, i) in gallery"
        :key="i"
        class="shrink-0 w-16 h-16 rounded-xl overflow-hidden border-2 transition-all"
        :class="i === activeIndex ? 'border-gold' : 'border-border hover:border-border-strong'"
        :aria-label="`Ver imagen ${i + 1}`"
        :aria-current="i === activeIndex"
        @click="select(i)"
      >
        <img :src="img" :alt="`${name} miniatura ${i + 1}`" class="w-full h-full object-cover" />
      </button>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-200"
        leave-active-class="transition-opacity duration-200"
        enter-from-class="opacity-0"
        leave-to-class="opacity-0"
      >
        <div
          v-if="lightboxOpen"
          class="fixed inset-0 z-[70] flex items-center justify-center bg-black/90 p-4"
          role="dialog"
          aria-modal="true"
          :aria-label="`Galería de ${name}`"
          @click.self="closeLightbox"
        >
          <button
            class="absolute top-4 right-4 text-text-secondary bg-surface-dim hover:bg-surface border border-border rounded-full p-3 transition-all z-10"
            aria-label="Cerrar galería"
            @click="closeLightbox"
          >
            <X :size="18" :stroke-width="2" />
          </button>

          <button
            v-if="hasMultiple"
            class="absolute left-4 text-text-secondary bg-surface-dim hover:bg-surface border border-border rounded-full p-3 transition-all"
            aria-label="Imagen anterior"
            @click.stop="prev"
          >
            <ChevronLeft :size="20" :stroke-width="2" />
          </button>

          <img
            :src="activeImage"
            :alt="`${name} — imagen ${activeIndex + 1}`"
            class="max-w-full max-h-[88vh] object-contain rounded-2xl"
          />

          <button
            v-if="hasMultiple"
            class="absolute right-4 text-text-secondary bg-surface-dim hover:bg-surface border border-border rounded-full p-3 transition-all"
            aria-label="Imagen siguiente"
            @click.stop="next"
          >
            <ChevronRight :size="20" :stroke-width="2" />
          </button>

          <div v-if="hasMultiple" class="absolute bottom-5 left-1/2 -translate-x-1/2 text-xs text-text-secondary font-mono">
            {{ activeIndex + 1 }} / {{ gallery.length }}
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>
