<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LogIn } from '@lucide/vue'

import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')

async function submit() {
  const ok = await authStore.login(email.value, password.value)
  if (ok) {
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    router.push(redirect)
  }
}
</script>

<template>
  <section class="py-16 sm:py-24 min-h-[70vh] flex items-center">
    <div class="max-w-md w-full mx-auto px-4">
      <div class="bento-card-static p-8 login-glass">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-semibold tracking-tight">Iniciar sesión</h1>
          <p class="text-text-secondary mt-2">Accede a tu cuenta para comprar y consultar tus pedidos.</p>
        </div>

        <form class="space-y-4" @submit.prevent="submit">
          <div>
            <label for="email" class="block text-sm font-medium text-text-secondary mb-1.5">Correo electrónico</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              placeholder="tu@correo.com"
              class="input-minimal"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-text-secondary mb-1.5">Contraseña</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              placeholder="••••••••"
              class="input-minimal"
            />
          </div>

          <p v-if="authStore.error" class="text-sm text-danger font-medium">
            {{ authStore.error }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-primary w-full flex items-center justify-center gap-2"
          >
            <LogIn :size="18" :stroke-width="2" />
            {{ authStore.loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <div class="mt-6 flex flex-col items-center gap-3">
          <router-link to="/forgot-password" class="btn-ghost text-sm">
            ¿Olvidaste tu contraseña?
          </router-link>
          <p class="text-sm text-text-secondary">
            ¿No tienes cuenta?
            <router-link to="/register" class="text-accent font-medium hover:underline">Regístrate aquí</router-link>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.login-glass {
  background: rgba(10, 10, 10, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: border-color 0.3s;
}
.login-glass:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}
</style>
