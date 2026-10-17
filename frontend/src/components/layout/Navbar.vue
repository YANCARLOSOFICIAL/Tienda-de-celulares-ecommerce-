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
  { label: 'Inicio', to: '/' },
  { label: 'Tienda', to: '/shop' },
  { label: 'Comparar', to: '/compare' },
]

function handleScroll() {
  isScrolled.value = window.scrollY > 20
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
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
  await authStore.fetchMe()
  if (authStore.isAuthenticated) {
    await cartStore.fetchCart()
  }
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
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
      'fixed top-0 left-0 w-full z-50 transition-colors duration-300 border-b',
      isScrolled
        ? 'bg-surface/95 backdrop-blur-xl border-border'
        : 'bg-surface border-transparent',
    ]"
  >
    <nav class="max-w-[1280px] mx-auto px-6" aria-label="Navegación principal">
      <div class="flex items-center justify-between h-[72px]">
        <router-link to="/" class="nav-logo">
          TIENDA<span class="nav-logo-accent">CELL</span>
        </router-link>

        <div class="hidden lg:flex items-center gap-8">
          <router-link
            v-for="link in navLinks"
            :key="link.label"
            :to="link.to"
            class="nav-link"
            :class="{ active: route.path === link.to }"
          >
            {{ link.label }}
          </router-link>
        </div>

        <div class="hidden lg:flex items-center gap-4 flex-1 max-w-xs mx-6">
          <PredictiveSearch />
        </div>

        <div class="hidden lg:flex items-center gap-1">
          <button class="nav-icon relative" aria-label="Ver carrito" @click="goToCart">
            <ShoppingCart :size="18" :stroke-width="1.5" />
            <span v-if="cartStore.itemCount > 0" class="nav-badge">{{ cartStore.itemCount }}</span>
          </button>

          <div v-if="authStore.isAuthenticated" class="relative user-menu-container">
            <button class="nav-user" @click.stop="isUserMenuOpen = !isUserMenuOpen">
              <User :size="16" :stroke-width="1.5" />
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
              <div v-if="isUserMenuOpen" class="dropdown absolute right-0 mt-2 w-52">
                <router-link to="/orders" class="dropdown-item" @click="isUserMenuOpen = false">
                  <Package :size="15" :stroke-width="1.5" />
                  Mis pedidos
                </router-link>
                <router-link to="/wishlist" class="dropdown-item" @click="isUserMenuOpen = false">
                  <Heart :size="15" :stroke-width="1.5" />
                  Mis favoritos
                </router-link>
                <router-link to="/profile" class="dropdown-item" @click="isUserMenuOpen = false">
                  <User :size="15" :stroke-width="1.5" />
                  Mi perfil
                </router-link>
                <router-link v-if="authStore.isAdmin" to="/admin" class="dropdown-item" @click="isUserMenuOpen = false">
                  <Shield :size="15" :stroke-width="1.5" />
                  Panel admin
                </router-link>
                <div class="my-1 h-px bg-border" />
                <button class="dropdown-item text-danger hover:bg-danger/10" @click="logout">
                  <LogOut :size="15" :stroke-width="1.5" />
                  Cerrar sesión
                </button>
              </div>
            </Transition>
          </div>

          <router-link v-else to="/login" class="btn-fill nav-cta">
            Entrar
          </router-link>
        </div>

        <div class="flex lg:hidden items-center gap-1">
          <button class="nav-icon relative" aria-label="Ver carrito" @click="goToCart">
            <ShoppingCart :size="18" :stroke-width="1.5" />
            <span v-if="cartStore.itemCount > 0" class="nav-badge">{{ cartStore.itemCount }}</span>
          </button>
          <button
            class="nav-icon"
            :aria-label="isMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
            :aria-expanded="isMenuOpen"
            @click="isMenuOpen = !isMenuOpen"
          >
            <Menu v-if="!isMenuOpen" :size="20" :stroke-width="1.5" />
            <X v-else :size="20" :stroke-width="1.5" />
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
        <div v-show="isMenuOpen" class="lg:hidden pb-6 border-t border-border pt-4">
          <div class="space-y-1 mb-4">
            <router-link
              v-for="link in navLinks"
              :key="link.label"
              :to="link.to"
              class="mobile-link"
              @click="isMenuOpen = false"
            >
              {{ link.label }}
            </router-link>
          </div>

          <div class="pt-4 border-t border-border space-y-1">
            <template v-if="authStore.isAuthenticated">
              <router-link to="/orders" class="mobile-link" @click="isMenuOpen = false">
                <Package :size="16" :stroke-width="1.5" />
                Mis pedidos
              </router-link>
              <router-link to="/wishlist" class="mobile-link" @click="isMenuOpen = false">
                <Heart :size="16" :stroke-width="1.5" />
                Mis favoritos
              </router-link>
              <router-link to="/profile" class="mobile-link" @click="isMenuOpen = false">
                <User :size="16" :stroke-width="1.5" />
                Mi perfil
              </router-link>
              <router-link v-if="authStore.isAdmin" to="/admin" class="mobile-link" @click="isMenuOpen = false">
                <Shield :size="16" :stroke-width="1.5" />
                Panel admin
              </router-link>
              <button class="mobile-link text-danger" @click="logout">
                <LogOut :size="16" :stroke-width="1.5" />
                Cerrar sesión
              </button>
            </template>
            <router-link v-else to="/login" class="btn-fill w-full mt-2" @click="isMenuOpen = false">
              Entrar
            </router-link>
          </div>
        </div>
      </Transition>
    </nav>
  </header>

  <div class="h-[72px]" aria-hidden="true"></div>
</template>

<style scoped>
.nav-logo {
  font-family: var(--font-family-serif);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.22em;
  color: var(--color-text);
  text-decoration: none;
}

.nav-logo-accent {
  color: var(--color-accent);
}

.nav-link {
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.25s ease;
  cursor: pointer;
  padding: 4px 0;
  border-bottom: 1px solid transparent;
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-accent);
}

.nav-link.active {
  border-bottom-color: var(--color-accent);
}

.nav-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--color-text-secondary);
  transition: color 0.25s ease, background 0.25s ease;
  cursor: pointer;
}

.nav-icon:hover {
  color: var(--color-accent);
  background: rgba(240, 196, 25, 0.06);
}

.nav-badge {
  position: absolute;
  top: 4px;
  right: 2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: var(--color-accent);
  color: #0a0906;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  transition: color 0.25s ease, background 0.25s ease;
  cursor: pointer;
}

.nav-user:hover {
  color: var(--color-accent);
  background: rgba(240, 196, 25, 0.06);
}

.nav-cta {
  padding: 10px 20px;
  font-size: 12px;
}

.dropdown {
  background: var(--color-surface-dim);
  border: 1px solid var(--color-border);
  border-radius: 0;
  overflow: hidden;
  box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.6);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 11px 16px;
  font-size: 13px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.2s ease, background 0.2s ease;
  cursor: pointer;
}

.dropdown-item:hover {
  color: var(--color-accent);
  background: rgba(240, 196, 25, 0.05);
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: color 0.2s ease;
}

.mobile-link:hover {
  color: var(--color-accent);
}
</style>
