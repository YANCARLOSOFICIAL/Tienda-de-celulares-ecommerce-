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
    formError.value = 'Las contrasenas no coinciden.'
    return
  }
  if (password.value.length < 8) {
    formError.value = 'La contrasena debe tener al menos 8 caracteres.'
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
  <section class="py-16 sm:py-24 min-h-[70vh] flex items-center">
    <div class="max-w-md w-full mx-auto px-4">
      <div class="bento-card-static p-8 register-glass">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-semibold tracking-tight">Crear cuenta</h1>
          <p class="text-text-secondary mt-2">Regístrate para comprar en Tienda Cell.</p>
        </div>

        <form class="space-y-4" @submit.prevent="submit">
          <div>
            <label for="full_name" class="block text-sm font-medium text-text-secondary mb-1.5">Nombre completo</label>
            <input
              id="full_name"
              v-model="fullName"
              type="text"
              required
              autocomplete="name"
              placeholder="Tu nombre"
              class="input-minimal"
            />
          </div>
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
              autocomplete="new-password"
              placeholder="Mínimo 8 caracteres"
              class="input-minimal"
            />
          </div>
          <div>
            <label for="confirm_password" class="block text-sm font-medium text-text-secondary mb-1.5">Confirmar contraseña</label>
            <input
              id="confirm_password"
              v-model="confirmPassword"
              type="password"
              required
              autocomplete="new-password"
              placeholder="Repite tu contraseña"
              class="input-minimal"
            />
          </div>

          <p v-if="formError" class="text-sm text-danger font-medium">
            {{ formError }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-primary w-full flex items-center justify-center gap-2"
          >
            <UserPlus :size="18" :stroke-width="2" />
            {{ authStore.loading ? 'Creando...' : 'Crear cuenta' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-text-secondary">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="text-accent font-medium hover:underline">Inicia sesión</router-link>
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.register-glass {
  background: rgba(10, 10, 10, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: border-color 0.3s;
}
.register-glass:focus-within {
  border-color: var(--color-accent);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
}
</style>
