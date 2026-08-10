<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, X, Smartphone, ShoppingCart, User } from '@lucide/vue'

import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const isMenuOpen = ref(false)
const isScrolled = ref(false)
const isUserMenuOpen = ref(false)

const navLinks = [
  { label: 'Inicio', href: '#hero' },
  { label: 'Catálogo', href: '#productos' },
  { label: 'Promociones', href: '#productos' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Contacto', href: '#contacto' },
]

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

function scrollToSection(href: string) {
  isMenuOpen.value = false
  if (route.name !== 'Home') {
    router.push('/').then(() => {
      setTimeout(() => {
        const el = document.querySelector(href)
        if (el) el.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    })
    return
  }
  const el = document.querySelector(href)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

function goToCart() {
  isMenuOpen.value = false
  router.push('/cart')
}

function logout() {
  authStore.logout()
  cartStore.itemCount = 0
  isUserMenuOpen.value = false
  router.push('/')
}

if (typeof window !== 'undefined') {
  window.addEventListener('scroll', handleScroll, { passive: true })
}

onMounted(async () => {
  await authStore.fetchMe()
  if (authStore.isAuthenticated) {
    await cartStore.fetchCart()
  }
})

watch(route, () => {
  isMenuOpen.value = false
  isUserMenuOpen.value = false
})
</script>

<template>
  <header
    :class="[
      'fixed top-0 left-0 w-full z-50 transition-all duration-300',
      isScrolled ? 'bg-brutal-white brutal-border border-t-0 border-l-0 border-r-0' : 'bg-brutal-white/90'
    ]"
  >
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" aria-label="Navegación principal">
      <div class="flex items-center justify-between h-16 lg:h-20">
        <a
          href="#hero"
          class="flex items-center gap-2 font-black text-xl lg:text-2xl tracking-tight hover:opacity-80 transition-opacity"
          @click.prevent="scrollToSection('#hero')"
        >
          <span class="bg-brutal-yellow brutal-border p-1.5 flex items-center justify-center">
            <Smartphone :size="24" :stroke-width="2.5" class="text-brutal-black" />
          </span>
          <span class="text-brutal-black">TIENDA<span class="text-brutal-yellow">CELL</span></span>
        </a>

        <div class="hidden lg:flex items-center gap-1">
          <a
            v-for="link in navLinks"
            :key="link.label"
            :href="link.href"
            class="px-4 py-2 font-bold text-sm uppercase tracking-wide hover:bg-brutal-yellow hover:brutal-border hover:brutal-shadow-sm transition-all"
            @click.prevent="scrollToSection(link.href)"
          >
            {{ link.label }}
          </a>

          <button
            class="ml-2 flex items-center gap-2 brutal-border px-3 py-2 font-bold text-sm uppercase tracking-wide hover:bg-brutal-yellow transition-colors relative"
            aria-label="Ver carrito"
            @click="goToCart"
          >
            <ShoppingCart :size="18" :stroke-width="2.5" />
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-2 -right-2 bg-brutal-black text-brutal-white text-[10px] font-black px-1.5 py-0.5 brutal-border min-w-[22px] text-center"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>

          <div v-if="authStore.isAuthenticated" class="relative ml-1">
            <button
              class="flex items-center gap-2 px-3 py-2 font-bold text-sm uppercase tracking-wide hover:bg-brutal-yellow brutal-border transition-colors"
              @click="isUserMenuOpen = !isUserMenuOpen"
            >
              <User :size="18" :stroke-width="2.5" />
              <span class="max-w-[120px] truncate">{{ authStore.user?.full_name }}</span>
            </button>
            <div
              v-if="isUserMenuOpen"
              class="absolute right-0 mt-2 w-52 bg-brutal-white brutal-border brutal-shadow"
            >
              <router-link to="/orders" class="block px-4 py-3 font-bold text-sm uppercase hover:bg-brutal-yellow">
                Mis pedidos
              </router-link>
              <router-link
                v-if="authStore.isAdmin"
                to="/admin"
                class="block px-4 py-3 font-bold text-sm uppercase hover:bg-brutal-yellow"
              >
                Panel admin
              </router-link>
              <button
                class="block w-full text-left px-4 py-3 font-bold text-sm uppercase hover:bg-brutal-yellow"
                @click="logout"
              >
                Cerrar sesión
              </button>
            </div>
          </div>

          <router-link
            v-else
            to="/login"
            class="ml-2 bg-brutal-black text-brutal-white brutal-border brutal-shadow-sm px-4 py-2 font-bold text-sm uppercase tracking-wide hover:bg-brutal-yellow hover:text-brutal-black transition-all"
          >
            Entrar
          </router-link>
        </div>

        <button
          class="lg:hidden brutal-border p-2 bg-brutal-yellow hover:bg-brutal-black hover:text-brutal-yellow transition-colors relative"
          @click="isMenuOpen = !isMenuOpen"
          :aria-label="isMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
          :aria-expanded="isMenuOpen"
        >
          <Menu v-if="!isMenuOpen" :size="24" :stroke-width="2.5" />
          <X v-else :size="24" :stroke-width="2.5" />
          <span
            v-if="cartStore.itemCount > 0 && !isMenuOpen"
            class="absolute -top-2 -right-2 bg-brutal-black text-brutal-white text-[10px] font-black px-1.5 py-0.5 brutal-border min-w-[22px] text-center"
          >
            {{ cartStore.itemCount }}
          </span>
        </button>
      </div>

      <div
        v-show="isMenuOpen"
        class="lg:hidden border-t-4 border-brutal-black py-4 space-y-2"
      >
        <a
          v-for="link in navLinks"
          :key="link.label"
          :href="link.href"
          class="block px-4 py-3 font-bold text-base uppercase tracking-wide hover:bg-brutal-yellow brutal-border transition-all"
          @click.prevent="scrollToSection(link.href)"
        >
          {{ link.label }}
        </a>
        <button
          class="flex items-center gap-2 w-full px-4 py-3 font-bold text-base uppercase tracking-wide brutal-border bg-brutal-white hover:bg-brutal-yellow transition-all"
          @click="goToCart"
        >
          <ShoppingCart :size="20" :stroke-width="2.5" />
          Mi carrito
          <span v-if="cartStore.itemCount > 0" class="bg-brutal-black text-brutal-white px-2 py-0.5 text-xs font-black ml-auto">
            {{ cartStore.itemCount }}
          </span>
        </button>
        <template v-if="authStore.isAuthenticated">
          <router-link
            to="/orders"
            class="flex items-center gap-2 w-full px-4 py-3 font-bold text-base uppercase tracking-wide brutal-border bg-brutal-white hover:bg-brutal-yellow transition-all"
          >
            <User :size="20" :stroke-width="2.5" />
            Mis pedidos
          </router-link>
          <router-link
            v-if="authStore.isAdmin"
            to="/admin"
            class="flex items-center gap-2 w-full px-4 py-3 font-bold text-base uppercase tracking-wide brutal-border bg-brutal-white hover:bg-brutal-yellow transition-all"
          >
            <User :size="20" :stroke-width="2.5" />
            Panel admin
          </router-link>
          <button
            class="block w-full px-4 py-3 font-bold text-base uppercase tracking-wide brutal-border bg-brutal-black text-brutal-white hover:bg-brutal-yellow hover:text-brutal-black transition-all"
            @click="logout"
          >
            Cerrar sesión
          </button>
        </template>
        <router-link
          v-else
          to="/login"
          class="flex items-center gap-2 w-full px-4 py-3 font-bold text-base uppercase tracking-wide brutal-border bg-brutal-black text-brutal-white hover:bg-brutal-yellow hover:text-brutal-black transition-all"
        >
          <User :size="20" :stroke-width="2.5" />
          Entrar
        </router-link>
      </div>
    </nav>
  </header>

  <div class="h-16 lg:h-20" aria-hidden="true"></div>
</template>
