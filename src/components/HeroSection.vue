<script setup lang="ts">
import { ChevronRight, Smartphone } from '@lucide/vue'

function scrollToSection(id: string) {
  const el = document.querySelector(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <section id="hero" class="relative overflow-hidden bg-surface dark">
    <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(circle at 25% 25%, #3B82F6 1px, transparent 1px); background-size: 48px 48px;"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-20 lg:py-28">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
        <div class="space-y-8 relative z-10">
          <span class="badge badge-accent">
            <span class="inline-block w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
            Envíos a todo el país
          </span>

          <h1 class="section-title leading-[1.05]">
            <span class="block text-white">Tu próximo</span>
            <span class="block text-blue-500">celular</span>
            <span class="block text-white">te espera</span>
          </h1>

          <p class="section-subtitle">
            Los mejores smartphones con los precios más competitivos. Marcas oficiales, garantía y atención personalizada.
          </p>

          <div class="flex flex-wrap gap-4">
            <a
              href="#productos"
              class="btn-primary inline-flex items-center gap-2"
              @click.prevent="scrollToSection('#productos')"
            >
              Comprar ahora
              <ChevronRight :size="18" :stroke-width="2.5" />
            </a>
            <a
              href="#productos"
              class="btn-secondary"
              @click.prevent="scrollToSection('#productos')"
            >
              Ver catálogo
            </a>
          </div>

          <div class="flex items-center gap-4 pt-2">
            <div class="flex -space-x-2">
              <div v-for="i in 4" :key="i" class="w-8 h-8 rounded-full border-2 border-surface bg-surface-dim flex items-center justify-center text-[10px] font-semibold text-text-secondary" :style="{ zIndex: 4 - i }">
                {{ ['M','C','R','A'][i-1] }}
              </div>
            </div>
            <span class="text-sm text-text-secondary">+2,500 clientes satisfechos</span>
          </div>
        </div>

        <div class="relative flex justify-center lg:justify-end">
          <div class="relative w-full max-w-sm">
            <div class="bento-card p-6 sm:p-8 animate-float" style="animation-delay: 0.5s;">
              <div class="aspect-[9/16] bg-surface-dim rounded-2xl flex flex-col items-center justify-center p-6 text-center border border-border">
                <div class="w-20 h-20 rounded-3xl bg-blue-500/10 flex items-center justify-center mb-4">
                  <Smartphone :size="40" :stroke-width="1.5" class="text-blue-500" />
                </div>
                <span class="font-bold text-xl text-white">iPhone 16</span>
                <span class="text-text-secondary text-sm">Pro Max</span>
                <span class="font-bold text-2xl text-blue-500 mt-4">$28,999</span>
                <span class="text-text-tertiary line-through text-sm">$32,999</span>
                <span class="mt-4 badge badge-accent">12% OFF</span>
              </div>
            </div>
            <div class="absolute -bottom-3 -left-3 bg-whatsapp text-white font-semibold text-xs px-4 py-2 rounded-2xl shadow-lg z-20">
              ¡Oferta exclusiva!
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
