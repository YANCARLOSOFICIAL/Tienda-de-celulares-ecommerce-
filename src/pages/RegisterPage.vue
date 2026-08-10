<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserPlus } from '@lucide/vue'

import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const formError = ref<string | null>(null)

async function submit() {
  formError.value = null
  if (password.value !== confirmPassword.value) {
    formError.value = 'Las contraseñas no coinciden.'
    return
  }
  if (password.value.length < 8) {
    formError.value = 'La contraseña debe tener al menos 8 caracteres.'
    return
  }
  const ok = await authStore.register(email.value, fullName.value, password.value)
  if (ok) {
    await authStore.login(email.value, password.value)
    router.push('/')
  } else {
    formError.value = authStore.error
  }
}
</script>

<template>
  <section class="py-16 sm:py-24 bg-brutal-gray min-h-[70vh] flex items-center">
    <div class="max-w-md w-full mx-auto px-4">
      <div class="brutal-card p-8">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-6">
          NUEVA CUENTA
        </span>
        <h1 class="font-black text-3xl uppercase mb-2">Crear cuenta</h1>
        <p class="text-brutal-black/60 mb-8">Regístrate para comprar en Tienda Cell.</p>

        <form class="space-y-5" @submit.prevent="submit">
          <div>
            <label for="full_name" class="block font-bold text-sm uppercase mb-1">Nombre completo</label>
            <input
              id="full_name"
              v-model="fullName"
              type="text"
              required
              autocomplete="name"
              placeholder="Tu nombre"
              class="w-full border-4 border-brutal-black px-4 py-3 font-semibold focus:bg-brutal-yellow/10 outline-none"
            />
          </div>
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
              autocomplete="new-password"
              placeholder="Mínimo 8 caracteres"
              class="w-full border-4 border-brutal-black px-4 py-3 font-semibold focus:bg-brutal-yellow/10 outline-none"
            />
          </div>
          <div>
            <label for="confirm_password" class="block font-bold text-sm uppercase mb-1">Confirmar contraseña</label>
            <input
              id="confirm_password"
              v-model="confirmPassword"
              type="password"
              required
              autocomplete="new-password"
              placeholder="Repite tu contraseña"
              class="w-full border-4 border-brutal-black px-4 py-3 font-semibold focus:bg-brutal-yellow/10 outline-none"
            />
          </div>

          <p v-if="formError" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">
            {{ formError }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="brutal-button bg-brutal-yellow text-brutal-black w-full px-6 py-4 flex items-center justify-center gap-2 uppercase tracking-wide disabled:opacity-60"
          >
            <UserPlus :size="18" :stroke-width="2.5" />
            {{ authStore.loading ? 'Creando...' : 'Crear cuenta' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-brutal-black/70">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="font-black underline">Inicia sesión</router-link>
        </p>
      </div>
    </div>
  </section>
</template>
