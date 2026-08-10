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
    class="py-16 sm:py-20 lg:py-28 bg-brutal-black"
    aria-labelledby="servicios-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-4">
          SERVICIOS
        </span>
        <h2 id="servicios-title" class="section-title text-brutal-yellow mb-4">
          Todo lo que necesitas
        </h2>
        <p class="section-subtitle !text-brutal-white/70">
          Más que una tienda, somos tu centro de soluciones móviles.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
        <article
          v-for="(service, index) in services"
          :key="service.title"
          :class="[
            'brutal-card !bg-brutal-white p-6 sm:p-8 text-center flex flex-col items-center gap-4 group',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: `${index * 100}ms` }"
        >
          <div class="brutal-border bg-brutal-yellow p-4 group-hover:bg-brutal-black transition-colors duration-300">
            <component :is="service.icon" :size="32" :stroke-width="2.5" class="text-brutal-black group-hover:text-brutal-yellow transition-colors duration-300" />
          </div>
          <h3 class="font-black text-xl">{{ service.title }}</h3>
          <p class="text-sm text-brutal-black/70">{{ service.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
