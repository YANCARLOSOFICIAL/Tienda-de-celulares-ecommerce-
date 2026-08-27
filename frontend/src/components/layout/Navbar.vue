<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, X, ShoppingCart, User, LogOut, Package, Heart, Shield } from '@lucide/vue'

import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import PredictiveSearch from '@/components/search/PredictiveSearch.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const isMenuOpen = ref(false)
const isScrolled = ref(false)
const isUserMenuOpen = ref(false)

const navLinks = [
  { label: 'Inicio', href: '#hero' },
  { label: 'Tienda', to: '/shop' },
  { label: 'Servicios', href: '#servicios' },
  { label: 'Contacto', href: '#contacto' },
]

function handleScroll() {
  isScrolled.value = window.scrollY > 10
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

function handleClickOutside(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('.user-menu-container')) {
    isUserMenuOpen.value = false
  }
}

onMounted(async () => {
  await authStore.fetchMe()
  if (authStore.isAuthenticated) {
    await cartStore.fetchCart()
  }
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
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
      isScrolled ? 'glass-strong shadow-2xl shadow-black/30' : 'bg-transparent'
    ]"
  >
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" aria-label="Navegacion principal">
      <div class="flex items-center justify-between h-14 lg:h-[76px]">
        <a
          href="#hero"
          class="flex items-center gap-3 text-white font-bold text-lg tracking-tight hover:opacity-70 transition-opacity"
          @click.prevent="scrollToSection('#hero')"
        >
          <span class="text-gold-gradient text-xl font-bold" style="font-family: var(--font-family-serif);">TC</span>
          Tienda Cell
        </a>

        <div class="hidden lg:flex items-center gap-9">
          <template v-for="link in navLinks" :key="link.label">
            <router-link
              v-if="link.to"
              :to="link.to"
              class="px-3 py-1.5 text-sm font-medium text-text-secondary hover:text-silver transition-colors rounded-lg"
            >
              {{ link.label }}
            </router-link>
            <a
              v-else
              :href="link.href"
              class="px-3 py-1.5 text-sm font-medium text-text-secondary hover:text-silver transition-colors rounded-lg"
              @click.prevent="scrollToSection(link.href!)"
            >
              {{ link.label }}
            </a>
          </template>
        </div>

        <div class="hidden lg:flex items-center gap-3 flex-1 max-w-md mx-4">
          <PredictiveSearch />
        </div>

        <div class="hidden lg:flex items-center gap-2">
          <button
            class="relative p-2 text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
            aria-label="Ver carrito"
            @click="goToCart"
          >
            <ShoppingCart :size="18" :stroke-width="1.75" />
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-gold text-[#0e0f12] text-[10px] font-semibold px-1.5 py-0.5 rounded-full min-w-[18px] text-center leading-none"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>

          <div v-if="authStore.isAuthenticated" class="relative user-menu-container">
            <button
              class="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
              @click.stop="isUserMenuOpen = !isUserMenuOpen"
            >
              <User :size="16" :stroke-width="1.75" />
              <span class="max-w-[100px] truncate">{{ authStore.user?.full_name }}</span>
            </button>
            <Transition
              enter-active-class="transition ease-out duration-150"
              enter-from-class="opacity-0 -translate-y-1"
              enter-to-class="opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-100"
              leave-from-class="opacity-100 translate-y-0"
              leave-to-class="opacity-0 -translate-y-1"
            >
              <div
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-1.5 w-52 glass-strong rounded-xl overflow-hidden shadow-2xl shadow-black/40"
              >
                <div class="py-1">
                  <router-link
                    to="/orders"
                    class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-secondary hover:text-white hover:bg-white/5 transition-colors"
                    @click="isUserMenuOpen = false"
                  >
                    <Package :size="15" :stroke-width="1.75" />
                    Mis pedidos
                  </router-link>
                  <router-link
                    to="/wishlist"
                    class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-secondary hover:text-white hover:bg-white/5 transition-colors"
                    @click="isUserMenuOpen = false"
                  >
                    <Heart :size="15" :stroke-width="1.75" />
                    Mis favoritos
                  </router-link>
                  <router-link
                    to="/profile"
                    class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-secondary hover:text-white hover:bg-white/5 transition-colors"
                    @click="isUserMenuOpen = false"
                  >
                    <User :size="15" :stroke-width="1.75" />
                    Mi perfil
                  </router-link>
                  <router-link
                    v-if="authStore.isAdmin"
                    to="/admin"
                    class="flex items-center gap-2.5 px-4 py-2.5 text-sm text-text-secondary hover:text-white hover:bg-white/5 transition-colors"
                    @click="isUserMenuOpen = false"
                  >
                    <Shield :size="15" :stroke-width="1.75" />
                    Panel admin
                  </router-link>
                  <div class="my-1 h-px bg-border" />
                  <button
                    class="flex items-center gap-2.5 w-full px-4 py-2.5 text-sm text-red-400 hover:bg-red-500/10 transition-colors"
                    @click="logout"
                  >
                    <LogOut :size="15" :stroke-width="1.75" />
                    Cerrar sesión
                  </button>
                </div>
              </div>
            </Transition>
          </div>

          <router-link
            v-else
            to="/login"
            class="btn-primary text-sm px-4 py-2"
          >
            Entrar
          </router-link>
        </div>

        <div class="flex lg:hidden items-center gap-2">
          <button
            class="relative p-2 text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
            aria-label="Ver carrito"
            @click="goToCart"
          >
            <ShoppingCart :size="18" :stroke-width="1.75" />
            <span
              v-if="cartStore.itemCount > 0"
              class="absolute -top-0.5 -right-0.5 bg-gold text-[#0e0f12] text-[10px] font-semibold px-1.5 py-0.5 rounded-full min-w-[18px] text-center leading-none"
            >
              {{ cartStore.itemCount }}
            </span>
          </button>

          <button
            class="p-2 text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
            @click="isMenuOpen = !isMenuOpen"
            :aria-label="isMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
            :aria-expanded="isMenuOpen"
          >
            <Menu v-if="!isMenuOpen" :size="20" :stroke-width="1.75" />
            <X v-else :size="20" :stroke-width="1.75" />
          </button>
        </div>
      </div>

      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div
          v-show="isMenuOpen"
          class="lg:hidden pb-4 glass-strong border-t border-white/10"
        >
          <div class="pt-3 space-y-1">
            <template v-for="link in navLinks" :key="link.label">
              <router-link
                v-if="link.to"
                :to="link.to"
                class="block px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click="isMenuOpen = false"
              >
                {{ link.label }}
              </router-link>
              <a
                v-else
                :href="link.href"
                class="block px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click.prevent="scrollToSection(link.href!)"
              >
                {{ link.label }}
              </a>
            </template>
          </div>

          <div class="mt-3 pt-3 border-t border-border space-y-1">
            <template v-if="authStore.isAuthenticated">
              <router-link
                to="/orders"
                class="flex items-center gap-2.5 px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click="isMenuOpen = false"
              >
                <Package :size="16" :stroke-width="1.75" />
                Mis pedidos
              </router-link>
              <router-link
                to="/wishlist"
                class="flex items-center gap-2.5 px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click="isMenuOpen = false"
              >
                <Heart :size="16" :stroke-width="1.75" />
                Mis favoritos
              </router-link>
              <router-link
                to="/profile"
                class="flex items-center gap-2.5 px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click="isMenuOpen = false"
              >
                <User :size="16" :stroke-width="1.75" />
                Mi perfil
              </router-link>
              <router-link
                v-if="authStore.isAdmin"
                to="/admin"
                class="flex items-center gap-2.5 px-3 py-2.5 text-sm font-medium text-text-secondary hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                @click="isMenuOpen = false"
              >
                <Shield :size="16" :stroke-width="1.75" />
                Panel admin
              </router-link>
              <button
                class="flex items-center gap-2.5 w-full px-3 py-2.5 text-sm font-medium text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                @click="logout"
              >
                <LogOut :size="16" :stroke-width="1.75" />
                Cerrar sesión
              </button>
            </template>
            <router-link
              v-else
              to="/login"
              class="flex items-center justify-center gap-2 w-full btn-primary text-sm"
              @click="isMenuOpen = false"
            >
              <User :size="16" :stroke-width="1.75" />
              Entrar
            </router-link>
          </div>
        </div>
      </Transition>
    </nav>
  </header>

  <div class="h-14 lg:h-16" aria-hidden="true"></div>
</template>
