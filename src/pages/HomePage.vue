<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ShoppingCart, Wrench, Shield, RefreshCcw, Headphones, Star, ChevronRight, MessageCircle } from '@lucide/vue'

import TrustIndicators from '../components/TrustIndicators.vue'

const featuredProducts = ref([
  { id: 1, name: 'iPhone 15 Pro Max', price: 1199, image: 'https://placehold.co/400x400/FAFAFA/1D1D1F?text=iPhone+15+Pro+Max&font=inter', badge: 'Nuevo' },
  { id: 2, name: 'Samsung Galaxy S24 Ultra', price: 1099, image: 'https://placehold.co/400x400/FAFAFA/1D1D1F?text=Galaxy+S24+Ultra&font=inter', badge: null },
  { id: 3, name: 'Xiaomi 14 Pro', price: 799, image: 'https://placehold.co/400x400/FAFAFA/1D1D1F?text=Xiaomi+14+Pro&font=inter', badge: 'Oferta' },
  { id: 4, name: 'Google Pixel 8 Pro', price: 899, image: 'https://placehold.co/400x400/FAFAFA/1D1D1F?text=Pixel+8+Pro&font=inter', badge: null },
])

const brands = ['Apple', 'Samsung', 'Xiaomi', 'Google', 'Motorola', 'OnePlus', 'Nothing']

const services = [
  { icon: Wrench, title: 'Reparacion', desc: 'Servicio tecnico rapido y confiable para todo tipo de celulares.' },
  { icon: Shield, title: 'Garantia', desc: 'Todos nuestros productos cuentan con garantia oficial.' },
  { icon: Headphones, title: 'Accesorios', desc: 'Fundas, cargadores, audifonos y mas.' },
  { icon: RefreshCcw, title: 'Intercambio', desc: 'Cambia tu celular actual por uno nuevo con descuento.' },
]

const testimonials = ref([
  { name: 'Maria L.', stars: 5, quote: 'Excelente atencion y precios muy buenos. Mi iPhone llego en perfecto estado.', avatar: 'M' },
  { name: 'Carlos R.', stars: 5, quote: 'Compre un Galaxy y quedo muy satisfecho. Lo recomiendo totalmente.', avatar: 'C' },
  { name: 'Ana P.', stars: 5, quote: 'El mejor lugar para comprar celulares. Rapidez y confianza.', avatar: 'A' },
])
</script>

<template>
  <!-- Hero Section -->
  <section class="section-clean bg-surface relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col lg:flex-row items-center gap-12 lg:gap-16 min-h-[70vh]">
        <div class="flex-1 text-center lg:text-left z-10">
          <span class="badge badge-accent mb-6 inline-flex">Nuevos 2024</span>
          <h1 class="section-title mb-6">
            Los mejores celulares<br />
            <span class="text-accent">al mejor precio</span>
          </h1>
          <p class="section-subtitle mb-8 mx-auto lg:mx-0">
            Encuentra tu proximo smartphone con los mejores precios del mercado.
            Envio gratis y garantia en todos los productos.
          </p>
          <RouterLink to="/tienda" class="btn-primary inline-flex items-center gap-2">
            <ShoppingCart :size="18" />
            Ver tienda
          </RouterLink>
        </div>

        <div class="flex-1 relative">
          <div class="relative w-full aspect-square max-w-md mx-auto">
            <div class="absolute inset-0 bg-gradient-to-br from-accent/10 to-accent/5 rounded-full blur-3xl"></div>
            <div class="relative z-10 w-full h-full flex items-center justify-center">
              <img
                src="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=800"
                alt="iPhone 15 Pro"
                class="w-4/5 h-4/5 object-contain animate-float drop-shadow-2xl"
              />
            </div>
            <div class="absolute top-10 right-10 glass-strong rounded-2xl p-4 animate-fade-in-up">
              <p class="text-sm font-semibold text-text">Envio gratis</p>
              <p class="text-xs text-text-secondary">En compras +$500</p>
            </div>
            <div class="absolute bottom-10 left-10 glass-strong rounded-2xl p-4 animate-fade-in-up" style="animation-delay: 0.2s">
              <p class="text-sm font-semibold text-text">6 meses</p>
              <p class="text-xs text-text-secondary">Sin intereses</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Products (Bento Grid) -->
  <section class="section-clean bg-surface-dim">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-end justify-between mb-10">
        <div>
          <h2 class="section-title">Lo mas vendido</h2>
          <p class="section-subtitle mt-2">Descubre nuestros smartphones mas populares</p>
        </div>
        <RouterLink to="/tienda" class="btn-ghost hidden sm:inline-flex items-center gap-1">
          Ver todo <ChevronRight :size="16" />
        </RouterLink>
      </div>

      <div class="bento-grid">
        <!-- Large featured card -->
        <RouterLink
          :to="`/producto/${featuredProducts[0].id}`"
          class="bento-card bento-span-2 bento-row-2 group cursor-pointer flex flex-col"
        >
          <div class="flex-1 bg-gradient-to-br from-surface-dim to-surface p-8 flex items-center justify-center relative overflow-hidden">
            <span v-if="featuredProducts[0].badge" class="absolute top-4 left-4 badge badge-accent z-10">
              {{ featuredProducts[0].badge }}
            </span>
            <img
              :src="featuredProducts[0].image"
              :alt="featuredProducts[0].name"
              class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-105"
            />
          </div>
          <div class="p-6">
            <h3 class="font-semibold text-lg text-text group-hover:text-accent transition-colors">
              {{ featuredProducts[0].name }}
            </h3>
            <p class="text-accent font-bold text-xl mt-1">${{ featuredProducts[0].price }}</p>
          </div>
        </RouterLink>

        <!-- Normal cards -->
        <RouterLink
          v-for="product in featuredProducts.slice(1)"
          :key="product.id"
          :to="`/producto/${product.id}`"
          class="bento-card group cursor-pointer"
        >
          <div class="bg-gradient-to-br from-surface-dim to-surface h-40 flex items-center justify-center relative overflow-hidden p-4">
            <span v-if="product.badge" class="absolute top-3 left-3 badge badge-accent text-[10px] z-10">
              {{ product.badge }}
            </span>
            <img
              :src="product.image"
              :alt="product.name"
              class="max-h-full max-w-full object-contain transition-transform duration-500 group-hover:scale-110"
            />
          </div>
          <div class="p-4">
            <h3 class="font-medium text-sm text-text group-hover:text-accent transition-colors line-clamp-1">
              {{ product.name }}
            </h3>
            <p class="text-accent font-bold mt-1">${{ product.price }}</p>
          </div>
        </RouterLink>
      </div>

      <div class="mt-8 text-center sm:hidden">
        <RouterLink to="/tienda" class="btn-ghost inline-flex items-center gap-1">
          Ver todo <ChevronRight :size="16" />
        </RouterLink>
      </div>
    </div>
  </section>

  <!-- Brands -->
  <section class="section-clean bg-surface">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="section-title text-center mb-10">Marcas que confiamos</h2>
      <div class="flex flex-wrap justify-center gap-8 sm:gap-12">
        <div
          v-for="brand in brands"
          :key="brand"
          class="text-text-secondary hover:text-text transition-all duration-300 cursor-pointer select-none"
        >
          <p class="text-2xl sm:text-3xl font-bold tracking-tight opacity-40 hover:opacity-100 transition-opacity">
            {{ brand }}
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Services -->
  <section class="section-clean bg-surface-dim">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="section-title">Nuestros servicios</h2>
        <p class="section-subtitle mt-2 mx-auto">Todo lo que necesitas en un solo lugar</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="(service, i) in services"
          :key="service.title"
          class="bento-card p-6 text-center group hover:border-accent/30 transition-colors"
        >
          <div class="w-16 h-16 rounded-full bg-surface-dim flex items-center justify-center mx-auto mb-4 group-hover:bg-accent/10 transition-colors">
            <component :is="service.icon" :size="28" class="text-accent" />
          </div>
          <h3 class="font-semibold text-lg text-text mb-2">{{ service.title }}</h3>
          <p class="text-sm text-text-secondary leading-relaxed">{{ service.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Trust Indicators -->
  <TrustIndicators />

  <!-- Testimonials -->
  <section class="section-clean bg-surface">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="section-title">Lo que dicen nuestros clientes</h2>
        <p class="section-subtitle mt-2 mx-auto">Experiencias reales de quienes confian en nosotros</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="t in testimonials"
          :key="t.name"
          class="glass-strong rounded-2xl p-6 transition-all duration-300 hover:shadow-lg"
        >
          <div class="flex gap-1 mb-4">
            <Star v-for="s in t.stars" :key="s" :size="16" class="text-warning fill-warning" />
          </div>
          <p class="text-text leading-relaxed mb-6 italic">"{{ t.quote }}"</p>
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
              <span class="text-accent font-bold text-sm">{{ t.avatar }}</span>
            </div>
            <span class="font-semibold text-text">{{ t.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Contact CTA -->
  <section class="section-clean bg-surface-dim">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bento-card p-8 sm:p-12 text-center">
        <div class="w-16 h-16 rounded-full bg-accent/10 flex items-center justify-center mx-auto mb-6">
          <MessageCircle :size="28" class="text-accent" />
        </div>
        <h2 class="section-title mb-4">Contactanos</h2>
        <p class="section-subtitle mx-auto mb-8">
          Tenes dudas? Escribinos por WhatsApp y te respondemos al instante. Estamos para ayudarte.
        </p>
        <a
          href="https://wa.me/5491112345678"
          target="_blank"
          rel="noopener"
          class="inline-flex items-center gap-2 bg-whatsapp text-white font-semibold px-8 py-3.5 rounded-full hover:opacity-90 transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg shadow-whatsapp/20"
        >
          <MessageCircle :size="20" />
          Chatea con nosotros
        </a>
      </div>
    </div>
  </section>

  <!-- Map -->
  <section class="section-clean bg-surface">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-8">
        <h2 class="section-title">Encontranos</h2>
        <p class="section-subtitle mt-2 mx-auto">Visitanos en nuestro local</p>
      </div>
      <div class="bento-card overflow-hidden p-2">
        <iframe
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3283.8403699704563!2d-58.3838!3d-34.6037!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95bccacdf8b0e405%3A0x5c68b39de097aa50!2sBuenos%20Aires%2C%20Argentina!5e0!3m2!1ses!2sar!4v1"
          width="100%"
          height="400"
          style="border: 0; border-radius: 16px"
          allowfullscreen
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
        />
      </div>
    </div>
  </section>
</template>
