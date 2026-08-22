<script setup lang="ts">
import { ref } from 'vue'
import { useTestimonialsStore } from '../stores/testimonials'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { Star } from '@lucide/vue'

const store = useTestimonialsStore()
const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)
</script>

<template>
  <section
    ref="sectionRef"
    class="section-clean bg-surface-dim"
    aria-labelledby="testimonios-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="badge badge-accent mb-4">Testimonios</span>
        <h2 id="testimonios-title" class="section-title mb-4">
          Lo que dicen nuestros clientes
        </h2>
        <p class="section-subtitle mx-auto">
          La satisfacción de nuestros clientes habla por sí sola.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="(testimonial, index) in store.testimonials"
          :key="testimonial.id"
          :class="[
            'rounded-2xl p-6 sm:p-8 flex flex-col bg-surface-dim border border-border',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 100}ms` }"
          itemscope
          itemtype="https://schema.org/Review"
        >
          <div class="flex items-center gap-0.5 mb-4" aria-label="Calificación">
            <Star
              v-for="i in 5"
              :key="i"
              :size="14"
              :stroke-width="2.5"
              :class="i <= testimonial.rating ? 'fill-warning text-warning' : 'text-border'"
            />
          </div>

          <blockquote class="flex-1 text-sm sm:text-base text-text-secondary mb-6 leading-relaxed">
            <span class="text-blue-500 text-lg font-bold">"</span>{{ testimonial.text }}<span class="text-blue-500 text-lg font-bold">"</span>
          </blockquote>

          <div class="flex items-center gap-3 mt-auto pt-4 border-t border-border">
            <img
              :src="testimonial.avatar"
              :alt="testimonial.name"
              loading="lazy"
              class="w-9 h-9 rounded-full object-cover border border-border"
            />
            <span class="font-medium text-sm text-white" itemprop="author">{{ testimonial.name }}</span>
          </div>
          <meta itemprop="reviewBody" :content="testimonial.text" />
        </article>
      </div>
    </div>
  </section>
</template>
