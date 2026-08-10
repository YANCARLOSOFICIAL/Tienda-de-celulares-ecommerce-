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
    class="py-16 sm:py-20 lg:py-28 bg-brutal-gray"
    aria-labelledby="testimonios-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-4">
          TESTIMONIOS
        </span>
        <h2 id="testimonios-title" class="section-title text-brutal-black mb-4">
          Lo que dicen nuestros clientes
        </h2>
        <p class="section-subtitle">
          La satisfacción de nuestros clientes habla por sí sola.
        </p>
      </div>

      <div
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8"
      >
        <article
          v-for="(testimonial, index) in store.testimonials"
          :key="testimonial.id"
          :class="[
            'brutal-card !bg-brutal-white p-6 sm:p-8 flex flex-col',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 100}ms` }"
          itemscope
          itemtype="https://schema.org/Review"
        >
          <div class="flex items-center gap-1 mb-4" aria-label="Calificación">
            <Star
              v-for="i in 5"
              :key="i"
              :size="16"
              :stroke-width="2.5"
              :class="i <= testimonial.rating ? 'fill-brutal-yellow text-brutal-yellow' : 'text-brutal-black/20'"
            />
          </div>

          <blockquote class="flex-1 text-sm sm:text-base text-brutal-black/80 mb-4 leading-relaxed">
            "{{ testimonial.text }}"
          </blockquote>

          <div class="flex items-center gap-3 mt-auto pt-4 border-t-4 border-brutal-black">
            <img
              :src="testimonial.avatar"
              :alt="testimonial.name"
              loading="lazy"
              class="w-10 h-10 rounded-full brutal-border object-cover"
            />
            <div>
              <span class="font-black text-sm" itemprop="author">{{ testimonial.name }}</span>
            </div>
          </div>
          <meta itemprop="reviewBody" :content="testimonial.text" />
        </article>
      </div>
    </div>
  </section>
</template>
