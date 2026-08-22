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
      class="fixed bottom-6 right-6 z-40 bg-whatsapp text-white rounded-full p-4 shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300 animate-pulse-whatsapp whatsapp-neon"
      aria-label="Contactar por WhatsApp"
    >
      <MessageCircle :size="28" :stroke-width="2" />
    </a>
  </Teleport>
</template>

<style scoped>
.whatsapp-neon {
  box-shadow: 0 0 15px rgba(37, 211, 102, 0.5), 0 0 30px rgba(37, 211, 102, 0.2);
}
.whatsapp-neon:hover {
  box-shadow: 0 0 20px rgba(37, 211, 102, 0.6), 0 0 40px rgba(37, 211, 102, 0.3);
}
</style>
