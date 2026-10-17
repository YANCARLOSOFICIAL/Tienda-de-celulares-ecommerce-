<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/layout/Navbar.vue'
import Footer from '@/components/layout/Footer.vue'
import WhatsAppButton from '@/components/layout/WhatsAppButton.vue'
import BackToTop from '@/components/layout/BackToTop.vue'
import Toaster from '@/components/layout/Toaster.vue'
import CompareBar from '@/components/compare/CompareBar.vue'

const route = useRoute()
// La Home es una landing editorial autocontenida (nav + footer propios tipo maison)
const isLanding = computed(() => route.name === 'Home')
</script>

<template>
  <div class="min-h-screen bg-surface flex flex-col">
    <Navbar v-if="!isLanding" />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer v-if="!isLanding" />
    <WhatsAppButton />
    <BackToTop />
    <CompareBar />
    <Toaster />
  </div>
</template>
