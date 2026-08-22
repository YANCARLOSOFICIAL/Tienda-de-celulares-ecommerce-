<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ShoppingCart, Wrench, Shield, RefreshCcw, Headphones, Star, ChevronRight, MessageCircle } from '@lucide/vue'

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
  <section id="hero" class="section-clean relative overflow-hidden" style="padding-top: 0; padding-bottom: 0;">
    <!-- Neural network canvas background -->
    <div class="absolute inset-0">
      <div class="absolute inset-0 bg-gradient-to-b from-surface-dim/40 to-surface-dim/78 z-[1]"></div>
      <div class="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[900px] h-[600px] pointer-events-none z-[2]"
        style="background: radial-gradient(ellipse at center, rgba(70,167,255,.20), transparent 55%);">
      </div>
      <div class="absolute inset-0 grid-overlay opacity-50 z-0"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-[3]">
      <div class="flex flex-col lg:flex-row items-center gap-12 lg:gap-16 min-h-[80vh] py-20">
        <div class="flex-1 text-center lg:text-left z-10">
          <span class="eyebrow mb-6 inline-flex">Celulares y tecnologia</span>
          <h1 class="mb-6" style="font-family: var(--font-family-serif); font-weight: 600; font-size: clamp(40px, 6vw, 64px); line-height: 1.05; letter-spacing: -0.02em;">
            Los mejores celulares
            <span class="text-gold-gradient">al mejor precio</span>
          </h1>
          <p class="text-text-secondary mb-8 mx-auto lg:mx-0" style="font-size: clamp(16px, 1.6vw, 19px); max-width: 560px;">
            Encuentra tu proximo smartphone con los mejores precios del mercado.
            Envio gratis y garantia en todos los productos.
          </p>
          <div class="flex gap-4 flex-wrap justify-center lg:justify-start">
            <RouterLink to="/shop" class="btn-primary">
              <ShoppingCart :size="18" />
              Ver tienda
            </RouterLink>
            <a href="#servicios" class="btn-secondary">
              Explorar servicios
            </a>
          </div>
          <div class="flex gap-12 mt-16 flex-wrap justify-center lg:justify-start">
            <div>
              <div class="text-gold-gradient text-3xl font-semibold" style="font-family: var(--font-family-serif);">24h</div>
              <div class="text-text-secondary text-sm mt-1">Envio express</div>
            </div>
            <div>
              <div class="text-gold-gradient text-3xl font-semibold" style="font-family: var(--font-family-serif);">100%</div>
              <div class="text-text-secondary text-sm mt-1">Garantia oficial</div>
            </div>
            <div>
              <div class="text-gold-gradient text-3xl font-semibold" style="font-family: var(--font-family-serif);">5k+</div>
              <div class="text-text-secondary text-sm mt-1">Clientes felices</div>
            </div>
          </div>
        </div>

        <div class="flex-1 relative">
          <div class="relative w-full aspect-square max-w-md mx-auto">
            <div class="absolute inset-0 rounded-full blur-3xl"
              style="background: radial-gradient(circle, rgba(217,169,47,.15), transparent 60%);"></div>
            <div class="relative z-10 w-full h-full flex items-center justify-center">
              <img
                src="https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-pro-finish-select-202309-6-7inch-naturaltitanium?wid=800"
                alt="iPhone 15 Pro"
                class="w-4/5 h-4/5 object-contain animate-float"
              />
            </div>
            <div class="absolute top-10 right-10 glass rounded-2xl p-4 animate-fade-in-up">
              <p class="text-sm font-semibold text-white">Envio gratis</p>
              <p class="text-xs text-text-secondary">En compras +$500</p>
            </div>
            <div class="absolute bottom-10 left-10 glass rounded-2xl p-4 animate-fade-in-up" style="animation-delay: 0.2s">
              <p class="text-sm font-semibold text-white">6 meses</p>
              <p class="text-xs text-text-secondary">Sin intereses</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Featured Products (Bento Grid) -->
  <section class="section-clean" id="productos">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-end justify-between mb-10">
        <div>
          <span class="eyebrow mb-3 inline-flex">Lo mas vendido</span>
          <h2 class="section-title">Descubre nuestros smartphones mas populares</h2>
        </div>
        <RouterLink to="/shop" class="view-all hidden sm:inline-flex">
          Ver todo
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </RouterLink>
      </div>

      <div class="bento-grid">
        <!-- Large featured card -->
        <RouterLink
          :to="`/products/${featuredProducts[0].id}`"
          class="bento-card bento-span-2 bento-row-2 group cursor-pointer flex flex-col"
        >
          <div class="flex-1 p-8 flex items-center justify-center relative overflow-hidden"
            style="background: linear-gradient(145deg, #0a1018, #163b65 42%, #1e6daf 68%, #a97718 130%);">
            <div class="absolute inset-0"
              style="background-image: linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px); background-size: 36px 36px;">
            </div>
            <span v-if="featuredProducts[0].badge" class="absolute top-4 left-4 badge badge-gold z-10">
              {{ featuredProducts[0].badge }}
            </span>
            <img
              :src="featuredProducts[0].image"
              :alt="featuredProducts[0].name"
              class="w-full h-full object-contain transition-transform duration-500 ease-out group-hover:scale-110 relative z-10"
            />
          </div>
          <div class="p-6">
            <h3 class="font-semibold text-lg text-white group-hover:text-gold-light transition-colors duration-300" style="font-family: var(--font-family-serif);">
              {{ featuredProducts[0].name }}
            </h3>
            <p class="text-gold font-bold text-xl mt-1">${{ featuredProducts[0].price }}</p>
          </div>
        </RouterLink>

        <!-- Normal cards -->
        <RouterLink
          v-for="product in featuredProducts.slice(1)"
          :key="product.id"
          :to="`/products/${product.id}`"
          class="bento-card group cursor-pointer"
        >
          <div class="h-40 flex items-center justify-center relative overflow-hidden p-4"
            style="background: linear-gradient(145deg, #0c1018, #1a2744 45%, #2a4068 70%, #1a1a1a);">
            <span v-if="product.badge" class="absolute top-3 left-3 badge badge-gold text-[10px] z-10">
              {{ product.badge }}
            </span>
            <img
              :src="product.image"
              :alt="product.name"
              class="max-h-full max-w-full object-contain transition-transform duration-500 ease-out group-hover:scale-110"
            />
          </div>
          <div class="p-4">
            <h3 class="font-medium text-sm text-white group-hover:text-gold-light transition-colors duration-300 line-clamp-1" style="font-family: var(--font-family-serif);">
              {{ product.name }}
            </h3>
            <p class="text-gold font-bold mt-1">${{ product.price }}</p>
          </div>
        </RouterLink>
      </div>

      <div class="mt-8 text-center sm:hidden">
        <RouterLink to="/shop" class="view-all inline-flex">
          Ver todo
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </RouterLink>
      </div>
    </div>
  </section>

  <!-- Brands -->
  <section class="section-clean" style="border-top: 1px solid var(--color-border); border-bottom: 1px solid var(--color-border);">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-10">
        <span class="eyebrow mb-3 inline-flex">Marcas</span>
        <h2 class="section-title">Confiado por las mejores marcas</h2>
      </div>
      <div class="flex flex-wrap justify-center gap-8 sm:gap-12">
        <div
          v-for="brand in brands"
          :key="brand"
          class="text-text-tertiary hover:text-silver transition-all duration-300 cursor-pointer select-none"
        >
          <p class="text-2xl sm:text-3xl font-bold tracking-tight opacity-40 hover:opacity-100 transition-opacity" style="font-family: var(--font-family-serif);">
            {{ brand }}
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- Services -->
  <section class="section-clean" id="servicios">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <span class="eyebrow mb-3 inline-flex">Servicios</span>
        <h2 class="section-title">Todo lo que necesitas en un solo lugar</h2>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="(service, i) in services"
          :key="service.title"
          class="bento-card p-6 text-center group"
        >
          <div class="w-16 h-16 rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-all duration-300"
            style="background: var(--color-metal-gradient, linear-gradient(135deg, #f8fafb 0%, #aebac5 25%, #ffffff 46%, #6d7b88 74%, #dbe3e9 100%)); border: 1px solid rgba(217,169,47,.55);">
            <component :is="service.icon" :size="28" class="text-[#102745]" />
          </div>
          <h3 class="font-semibold text-lg text-white mb-2" style="font-family: var(--font-family-serif);">{{ service.title }}</h3>
          <p class="text-sm text-text-secondary leading-relaxed">{{ service.desc }}</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Testimonials -->
  <section class="section-clean">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <span class="eyebrow mb-3 inline-flex">Testimonios</span>
        <h2 class="section-title">Lo que dicen nuestros clientes</h2>
        <p class="section-subtitle mt-2 mx-auto">Experiencias reales de quienes confian en nosotros</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div
          v-for="t in testimonials"
          :key="t.name"
          class="bento-card rounded-2xl p-6"
        >
          <div class="flex gap-1 mb-4">
            <Star v-for="s in t.stars" :key="s" :size="16" class="text-gold fill-gold" />
          </div>
          <p class="text-white leading-relaxed mb-6 italic">"{{ t.quote }}"</p>
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full flex items-center justify-center"
              style="background: var(--color-gradient, linear-gradient(115deg, #d8e0e7 0%, #7faee0 28%, #267dd1 52%, #0d315e 70%, #d6a52c 100%));">
              <span class="text-white font-bold text-sm">{{ t.avatar }}</span>
            </div>
            <span class="font-semibold text-white">{{ t.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Contact CTA -->
  <section class="section-clean" id="contacto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="bento-card p-8 sm:p-12 text-center relative overflow-hidden">
        <div class="absolute inset-0 opacity-38"
          style="background: linear-gradient(115deg, rgba(70,167,255,.40), rgba(217,169,47,.32));">
        </div>
        <div class="relative z-10">
          <div class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6"
            style="background: var(--color-metal-gradient, linear-gradient(135deg, #f8fafb 0%, #aebac5 25%, #ffffff 46%, #6d7b88 74%, #dbe3e9 100%));">
            <MessageCircle :size="28" class="text-[#102745]" />
          </div>
          <h2 class="section-title mb-4">Contactanos</h2>
          <p class="section-subtitle mx-auto mb-8">
            Tenes dudas? Escribinos por WhatsApp y te respondemos al instante. Estamos para ayudarte.
          </p>
          <a
            href="https://wa.me/5491112345678"
            target="_blank"
            rel="noopener"
            class="inline-flex items-center gap-2 bg-whatsapp text-white font-semibold px-8 py-3.5 rounded-full hover:opacity-90 transition-all duration-300 hover:scale-105 active:scale-95 shadow-lg shadow-whatsapp/20"
          >
            <MessageCircle :size="20" />
            Chatea con nosotros
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Map -->
  <section class="section-clean">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-8">
        <span class="eyebrow mb-3 inline-flex">Ubicacion</span>
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
