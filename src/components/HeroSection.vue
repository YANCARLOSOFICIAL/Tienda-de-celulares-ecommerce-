<script setup lang="ts">
import { ChevronRight, Smartphone } from '@lucide/vue'

function scrollToSection(id: string) {
  const el = document.querySelector(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <section id="hero" class="relative overflow-hidden bg-brutal-yellow">
    <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(circle at 25% 25%, #111 1px, transparent 1px); background-size: 40px 40px;"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24">
      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-center">
        <div class="space-y-6 lg:space-y-8 relative z-10">
          <div class="inline-block bg-brutal-black text-brutal-yellow font-bold text-sm px-4 py-2 brutal-border animate-float">
            <span class="inline-block w-2 h-2 bg-brutal-yellow rounded-full mr-2"></span>
            ENVÍOS A TODO EL PAÍS
          </div>

          <h1 class="section-title text-brutal-black leading-[0.9]">
            <span class="block">TU PRÓXIMO</span>
            <span class="block bg-brutal-black text-brutal-yellow inline-block px-2 pt-1">CELULAR</span>
            <span class="block">TE ESPERA</span>
          </h1>

          <p class="text-lg sm:text-xl font-medium text-brutal-black/80 max-w-lg">
            Los mejores smartphones con los precios más competitivos. Marcas oficiales, garantía y atención personalizada.
          </p>

          <div class="flex flex-wrap gap-4">
            <a
              href="#productos"
              class="brutal-button bg-brutal-black text-brutal-white px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg uppercase tracking-wide flex items-center gap-2"
              @click.prevent="scrollToSection('#productos')"
            >
              Comprar ahora
              <ChevronRight :size="20" :stroke-width="3" />
            </a>
            <a
              href="#productos"
              class="brutal-button bg-brutal-white text-brutal-black px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg uppercase tracking-wide"
              @click.prevent="scrollToSection('#productos')"
            >
              Ver catálogo
            </a>
          </div>

          <div class="flex items-center gap-6 pt-4">
            <div class="flex -space-x-2">
              <div v-for="i in 4" :key="i" class="w-8 h-8 rounded-full brutal-border border-2 border-brutal-white bg-brutal-gray flex items-center justify-center text-[10px] font-black" :style="{ zIndex: 4 - i }">
                {{ ['M','C','R','A'][i-1] }}
              </div>
            </div>
            <span class="font-bold text-sm">+2,500 clientes satisfechos</span>
          </div>
        </div>

        <div class="relative flex justify-center lg:justify-end">
          <div class="relative w-full max-w-md">
            <div class="brutal-card bg-brutal-black p-6 sm:p-8 animate-float" style="animation-delay: 0.5s;">
              <div class="aspect-[9/16] bg-brutal-yellow/10 brutal-border flex flex-col items-center justify-center p-4 text-center">
                <Smartphone :size="80" :stroke-width="1.5" class="text-brutal-yellow mb-4" />
                <span class="text-brutal-yellow font-black text-2xl">iPhone 16</span>
                <span class="text-brutal-white font-bold text-lg">Pro Max</span>
                <span class="text-brutal-yellow font-black text-3xl mt-4">$28,999</span>
                <span class="text-brutal-white/60 line-through text-sm">$32,999</span>
                <span class="mt-4 bg-brutal-yellow text-brutal-black font-bold px-4 py-1 brutal-border text-sm">12% OFF</span>
              </div>
            </div>
            <div class="absolute -bottom-4 -left-4 bg-whatsapp text-brutal-white font-black text-sm px-4 py-2 brutal-border brutal-shadow-yellow rotate-[-3deg] z-20">
              ¡OFERTA EXCLUSIVA!
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
