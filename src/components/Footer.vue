<script setup lang="ts">
import { Smartphone, Heart } from '@lucide/vue'

const footerLinks = {
  empresa: [
    { label: 'Inicio', href: '#hero' },
    { label: 'Catálogo', href: '#productos' },
    { label: 'Servicios', href: '#servicios' },
    { label: 'Contacto', href: '#contacto' },
  ],
  servicios: [
    { label: 'Reparación', href: '#servicios' },
    { label: 'Accesorios', href: '#servicios' },
    { label: 'Garantía', href: '#servicios' },
    { label: 'Compra y Venta', href: '#servicios' },
  ],
  contacto: [
    { label: '+52 123 456 7890' },
    { label: 'hola@tiendacell.mx' },
    { label: 'Av. Tecnológico 123, CDMX' },
  ]
}

function scrollToSection(href: string) {
  const el = document.querySelector(href)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <footer class="bg-brutal-black text-brutal-white border-t-4 border-brutal-yellow" role="contentinfo">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12">
        <div class="space-y-4">
          <a
            href="#hero"
            class="flex items-center gap-2 font-black text-xl tracking-tight"
            @click.prevent="scrollToSection('#hero')"
          >
            <span class="bg-brutal-yellow brutal-border p-1.5 flex items-center justify-center">
              <Smartphone :size="22" :stroke-width="2.5" class="text-brutal-black" />
            </span>
            <span>TIENDA<span class="text-brutal-yellow">CELL</span></span>
          </a>
          <p class="text-brutal-white/60 text-sm leading-relaxed">
            Tu tienda de celulares de confianza. Los mejores precios, marcas oficiales y atención personalizada.
          </p>
        </div>

        <div>
          <h3 class="font-black text-sm uppercase tracking-wider text-brutal-yellow mb-4">Empresa</h3>
          <ul class="space-y-2">
            <li v-for="link in footerLinks.empresa" :key="link.label">
              <a
                :href="link.href"
                class="text-brutal-white/70 hover:text-brutal-yellow font-medium text-sm transition-colors"
                @click.prevent="scrollToSection(link.href)"
              >
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>

        <div>
          <h3 class="font-black text-sm uppercase tracking-wider text-brutal-yellow mb-4">Servicios</h3>
          <ul class="space-y-2">
            <li v-for="link in footerLinks.servicios" :key="link.label">
              <a
                :href="link.href"
                class="text-brutal-white/70 hover:text-brutal-yellow font-medium text-sm transition-colors"
                @click.prevent="scrollToSection(link.href)"
              >
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>

        <div>
          <h3 class="font-black text-sm uppercase tracking-wider text-brutal-yellow mb-4">Contacto</h3>
          <ul class="space-y-2">
            <li v-for="item in footerLinks.contacto" :key="item.label">
              <span class="text-brutal-white/70 font-medium text-sm">{{ item.label }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="border-t-4 border-brutal-yellow/30 py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-brutal-white/50 text-sm">
          &copy; {{ new Date().getFullYear() }} Tienda Cell. Todos los derechos reservados.
        </p>
        <p class="text-brutal-white/50 text-sm flex items-center gap-1">
          Hecho con <Heart :size="14" class="text-red-500 fill-red-500" /> en México
        </p>
      </div>
    </div>
  </footer>
</template>
