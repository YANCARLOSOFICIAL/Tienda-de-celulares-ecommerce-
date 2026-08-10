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
  <section class="py-16 sm:py-24 bg-brutal-gray min-h-[70vh] flex items-center">
    <div class="max-w-md w-full mx-auto px-4">
      <div class="brutal-card p-8">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-6">
          ACCESO
        </span>
        <h1 class="font-black text-3xl uppercase mb-2">Iniciar sesión</h1>
        <p class="text-brutal-black/60 mb-8">Accede a tu cuenta para comprar y consultar tus pedidos.</p>

        <form class="space-y-5" @submit.prevent="submit">
          <div>
            <label for="email" class="block font-bold text-sm uppercase mb-1">Correo electrónico</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              placeholder="tu@correo.com"
              class="w-full border-4 border-brutal-black px-4 py-3 font-semibold focus:bg-brutal-yellow/10 outline-none"
            />
          </div>
          <div>
            <label for="password" class="block font-bold text-sm uppercase mb-1">Contraseña</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              placeholder="••••••••"
              class="w-full border-4 border-brutal-black px-4 py-3 font-semibold focus:bg-brutal-yellow/10 outline-none"
            />
          </div>

          <p v-if="authStore.error" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">
            {{ authStore.error }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="brutal-button bg-brutal-yellow text-brutal-black w-full px-6 py-4 flex items-center justify-center gap-2 uppercase tracking-wide disabled:opacity-60"
          >
            <LogIn :size="18" :stroke-width="2.5" />
            {{ authStore.loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-brutal-black/70">
          ¿No tienes cuenta?
          <router-link to="/register" class="font-black underline">Regístrate aquí</router-link>
        </p>
      </div>
    </div>
  </section>
</template>
