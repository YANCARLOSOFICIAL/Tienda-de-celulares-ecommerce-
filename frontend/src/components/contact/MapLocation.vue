<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
import { MapPin } from '@lucide/vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)
</script>

<template>
  <section
    ref="sectionRef"
    class="section-clean bg-surface"
    aria-label="Ubicación"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-10">
        <span class="badge badge-accent mb-4">Ubicación</span>
        <h2 class="section-title mb-4">
          Visítanos
        </h2>
        <p class="section-subtitle mx-auto flex items-center justify-center gap-2">
          <MapPin :size="16" :stroke-width="2" class="text-blue-500" />
          Av. Tecnológico 123, Col. Centro, CDMX
        </p>
      </div>

      <div
        :class="[
          'bento-card-static overflow-hidden rounded-2xl border border-border',
          'animate-fade-in-up',
          isVisible ? 'visible' : ''
        ]"
      >
        <div class="aspect-[21/9] min-h-[300px] bg-surface-dim">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3762.5!2d-99.1332!3d19.4326!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTnCsDI1JzU3LjQiTiA5OcKwMDgnMDAuMCJX!5e0!3m2!1ses!2smx!4v1"
            width="100%"
            height="100%"
            style="border:0; min-height: 300px;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
            title="Ubicación de Tienda Cell"
          ></iframe>
        </div>
      </div>
    </div>
  </section>
</template>
