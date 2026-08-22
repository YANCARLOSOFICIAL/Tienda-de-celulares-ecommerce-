<script setup lang="ts">
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import WhatsAppButton from './components/WhatsAppButton.vue'
import BackToTop from './components/BackToTop.vue'
import CompareBar from './components/CompareBar.vue'
</script>

<template>
  <div class="min-h-screen bg-surface-dim flex flex-col">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
    <WhatsAppButton />
    <BackToTop />
    <CompareBar />
  </div>
</template>
