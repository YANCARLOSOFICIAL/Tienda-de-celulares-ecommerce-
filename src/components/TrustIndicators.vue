<script setup lang="ts">
import { Shield, Truck, CreditCard, Headphones, RefreshCcw, Lock } from '@lucide/vue'

const indicators = [
  {
    icon: Shield,
    title: 'Garantía oficial',
    description: 'Todos los productos con garantía del fabricante',
    color: 'text-neon-blue',
    glow: 'shadow-[0_0_12px_rgba(0,212,255,0.3)]',
  },
  {
    icon: Truck,
    title: 'Envío gratis',
    description: 'En compras mayores a $999 MXN',
    color: 'text-neon-green',
    glow: 'shadow-[0_0_12px_rgba(0,255,136,0.3)]',
  },
  {
    icon: CreditCard,
    title: 'Meses sin intereses',
    description: 'Paga hasta en 12 MSI con tarjetas participantes',
    color: 'text-neon-purple',
    glow: 'shadow-[0_0_12px_rgba(191,90,242,0.3)]',
  },
  {
    icon: Lock,
    title: 'Pago seguro',
    description: 'Transacciones encriptadas y protegidas',
    color: 'text-warning',
    glow: 'shadow-[0_0_12px_rgba(255,214,10,0.3)]',
  },
  {
    icon: Headphones,
    title: 'Soporte 24/7',
    description: 'Atención personalizada cuando la necesites',
    color: 'text-accent',
    glow: 'shadow-[0_0_12px_rgba(0,212,255,0.3)]',
  },
  {
    icon: RefreshCcw,
    title: 'Devolución fácil',
    description: '30 días para cambios y devoluciones',
    color: 'text-success',
    glow: 'shadow-[0_0_12px_rgba(0,255,136,0.3)]',
  },
]
</script>

<template>
  <section class="section-clean bg-surface">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-10">
        <h2 class="section-title">¿Por qué elegirnos?</h2>
        <p class="section-subtitle mx-auto mt-3">Tu confianza es nuestra prioridad</p>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 md:gap-6">
        <div
          v-for="item in indicators"
          :key="item.title"
          class="bento-card p-5 md:p-6 text-center group"
        >
          <div
            class="w-12 h-12 rounded-2xl flex items-center justify-center mx-auto mb-4 transition-all duration-300 bg-surface-dim border border-border group-hover:scale-110"
            :class="[item.glow]"
          >
            <component :is="item.icon" :size="22" :stroke-width="1.75" :class="item.color" />
          </div>
          <h3 class="font-semibold text-sm md:text-base text-text mb-1">{{ item.title }}</h3>
          <p class="text-xs md:text-sm text-text-secondary leading-relaxed">{{ item.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>