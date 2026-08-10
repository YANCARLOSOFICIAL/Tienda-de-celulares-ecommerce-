<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ArrowUp } from '@lucide/vue'

const showButton = ref(false)

function handleScroll() {
  showButton.value = window.scrollY > 600
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <Teleport to="body">
    <button
      v-show="showButton"
      type="button"
      class="fixed bottom-6 left-6 z-40 bg-brutal-yellow text-brutal-black brutal-border brutal-shadow-sm p-4 hover:bg-brutal-black hover:text-brutal-yellow transition-all"
      :style="{ boxShadow: '4px 4px 0px #111111' }"
      @click="scrollToTop"
      aria-label="Volver arriba"
    >
      <ArrowUp :size="24" :stroke-width="3" />
    </button>
  </Teleport>
</template>
