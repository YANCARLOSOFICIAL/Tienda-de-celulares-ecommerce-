<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { MessageCircle } from '@lucide/vue'

const showButton = ref(false)

function handleScroll() {
  showButton.value = window.scrollY > 400
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
    <a
      v-show="showButton"
      href="https://wa.me/521234567890"
      target="_blank"
      rel="noopener noreferrer"
      class="fixed bottom-6 right-6 z-40 bg-whatsapp text-brutal-white brutal-border brutal-shadow-sm p-4 hover:brightness-110 transition-all animate-pulse-whatsapp"
      :style="{ boxShadow: '4px 4px 0px #111111' }"
      aria-label="Contactar por WhatsApp"
    >
      <MessageCircle :size="28" :stroke-width="2.5" />
    </a>
  </Teleport>
</template>
