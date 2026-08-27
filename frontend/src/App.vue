<script setup lang="ts">
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
import WhatsAppButton from '@/components/layout/WhatsAppButton.vue'
import BackToTop from '@/components/layout/BackToTop.vue'
import Toaster from '@/components/layout/Toaster.vue'
import CompareBar from '@/components/compare/CompareBar.vue'
</script>

<template>
  <div class="min-h-screen bg-surface flex flex-col">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
    <WhatsAppButton />
    <BackToTop />
    <CompareBar />
    <Toaster />
  </div>
</template>
