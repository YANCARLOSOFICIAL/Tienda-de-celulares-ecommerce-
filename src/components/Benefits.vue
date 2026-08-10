<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { Truck, ShieldCheck, LockKeyhole, Headset } from '@lucide/vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)

const benefits = [
  {
    icon: Truck,
    title: 'Envíos Rápidos',
    description: 'Entregas en 24-48 horas a todo el país. Seguimiento en tiempo real.'
  },
  {
    icon: ShieldCheck,
    title: 'Garantía Incluida',
    description: 'Todos nuestros productos cuentan con garantía oficial de fábrica.'
  },
  {
    icon: LockKeyhole,
    title: 'Pagos Seguros',
    description: 'Transferencia, tarjeta o efectivo. Todos tus datos protegidos.'
  },
  {
    icon: Headset,
    title: 'Atención Personalizada',
    description: 'Te asesoramos para encontrar el equipo perfecto para ti.'
  }
]
</script>

<template>
  <section
    ref="sectionRef"
    class="py-16 sm:py-20 bg-brutal-yellow"
    aria-label="Beneficios"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="inline-block bg-brutal-black text-brutal-yellow font-bold text-sm px-4 py-2 brutal-border mb-4">
          ¿POR QUÉ ELEGIRNOS?
        </span>
        <h2 class="section-title text-brutal-black mb-4">
          Beneficios Exclusivos
        </h2>
        <p class="section-subtitle">
          Te ofrecemos la mejor experiencia de compra en cada paso.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
        <article
          v-for="(benefit, index) in benefits"
          :key="benefit.title"
          :class="[
            'brutal-card !bg-brutal-white p-6 sm:p-8 flex flex-col items-center text-center gap-4',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 100}ms` }"
        >
          <div class="brutal-border bg-brutal-black p-4">
            <component :is="benefit.icon" :size="28" :stroke-width="2.5" class="text-brutal-yellow" />
          </div>
          <h3 class="font-black text-lg">{{ benefit.title }}</h3>
          <p class="text-sm text-brutal-black/70">{{ benefit.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
