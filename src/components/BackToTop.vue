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
      class="fixed bottom-6 left-6 z-40 bg-accent text-white rounded-full p-4 shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300 back-to-top-neon"
      @click="scrollToTop"
      aria-label="Volver arriba"
    >
      <ArrowUp :size="24" :stroke-width="2" />
    </button>
  </Teleport>
</template>

<style scoped>
.back-to-top-neon {
  box-shadow: 0 0 15px rgba(0, 212, 255, 0.4), 0 0 30px rgba(0, 212, 255, 0.15);
}
.back-to-top-neon:hover {
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.5), 0 0 50px rgba(0, 212, 255, 0.2);
}
</style>
