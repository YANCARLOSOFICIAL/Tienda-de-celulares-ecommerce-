<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { Wrench, Smartphone, ShieldCheck, RefreshCw } from '@lucide/vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)

const services = [
  {
    icon: Wrench,
    title: 'Reparación',
    description: 'Reparamos tu equipo con repuestos originales y garantía de 6 meses en todos nuestros servicios.'
  },
  {
    icon: Smartphone,
    title: 'Accesorios',
    description: 'Fundas, audífonos, cargadores, protectores de pantalla y más accesorios originales.'
  },
  {
    icon: ShieldCheck,
    title: 'Garantía',
    description: 'Todos nuestros productos incluyen garantía oficial. Respaldo y soporte técnico incluido.'
  },
  {
    icon: RefreshCw,
    title: 'Compra y Venta',
    description: 'Vendemos tu equipo usado y te ayudamos a renovarlo. ¡Te damos el mejor precio por tu celular!'
  }
]
</script>

<template>
  <section
    id="servicios"
    ref="sectionRef"
    class="section-clean bg-surface"
    aria-labelledby="servicios-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="badge badge-accent mb-4">Servicios</span>
        <h2 id="servicios-title" class="section-title mb-4">
          Todo lo que necesitas
        </h2>
        <p class="section-subtitle mx-auto">
          Más que una tienda, somos tu centro de soluciones móviles.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <article
          v-for="(service, index) in services"
          :key="service.title"
          :class="[
            'bento-card p-6 sm:p-8 text-center flex flex-col items-center gap-4 group',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 100}ms` }"
        >
          <div class="w-14 h-14 rounded-2xl bg-blue-500/10 flex items-center justify-center group-hover:bg-blue-500 transition-colors duration-300">
            <component :is="service.icon" :size="24" :stroke-width="2" class="text-blue-500 group-hover:text-white transition-colors duration-300" />
          </div>
          <h3 class="font-semibold text-base text-white">{{ service.title }}</h3>
          <p class="text-sm text-text-secondary leading-relaxed">{{ service.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
