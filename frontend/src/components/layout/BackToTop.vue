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
      class="fixed bottom-6 left-6 z-40 bg-blue-500 text-white rounded-full p-4 shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300"
      @click="scrollToTop"
      aria-label="Volver arriba"
    >
      <ArrowUp :size="24" :stroke-width="2" />
    </button>
  </Teleport>
</template>
