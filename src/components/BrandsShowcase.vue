<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)

const brands = [
  { name: 'Apple', logo: '', color: '#111' },
  { name: 'Samsung', logo: 'SAMSUNG', color: '#1428A0' },
  { name: 'Xiaomi', logo: 'XIAOMI', color: '#FF6900' },
  { name: 'Motorola', logo: 'MOTOROLA', color: '#A100FF' },
  { name: 'Honor', logo: 'HONOR', color: '#000' },
  { name: 'Oppo', logo: 'OPPO', color: '#1A6B37' },
]
</script>

<template>
  <section
    id="marcas"
    ref="sectionRef"
    class="section-clean bg-surface border-y border-border"
    aria-labelledby="marcas-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-10">
        <h2 id="marcas-title" class="section-title mb-4">
          Marcas Disponibles
        </h2>
        <p class="section-subtitle mx-auto">
          Trabajamos con las marcas más reconocidas del mercado.
        </p>
      </div>

      <div class="grid grid-cols-3 lg:grid-cols-6 gap-4">
        <div
          v-for="(brand, index) in brands"
          :key="brand.name"
          :class="[
            'bento-card-static flex items-center justify-center p-6 sm:p-8 min-h-[100px] sm:min-h-[120px] group cursor-default',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 80}ms` }"
        >
          <span
            class="font-bold text-center text-sm sm:text-base tracking-tight text-text-secondary group-hover:text-gold transition-colors duration-300"
            :style="{ '--brand-hover': brand.color }"
          >
            {{ brand.logo }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
