<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Lock, ArrowLeft, CheckCircle2 } from '@lucide/vue'

import { passwordResetApi } from '../api/passwordReset'

const route = useRoute()
const router = useRouter()

const token = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

onMounted(() => {
  const qToken = route.query.token
  if (qToken && typeof qToken === 'string') {
    token.value = qToken
  }
})

async function resetPassword() {
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Las contrasenas no coinciden'
    return
  }
  loading.value = true
  error.value = null
  try {
    await passwordResetApi.confirmPassword(token.value, newPassword.value)
    success.value = true
  } catch (e: any) {
    error.value = e.message || 'Error al restablecer la contrasena'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh] flex items-center">
    <div class="max-w-md mx-auto px-4 sm:px-6 w-full">
      <div class="brutal-card p-8">
        <div class="text-center mb-6">
          <span class="bg-brutal-yellow p-3 brutal-border inline-block mb-4">
            <Lock :size="24" :stroke-width="2.5" />
          </span>
          <h1 class="font-black text-2xl uppercase">Nueva contrasena</h1>
        </div>

        <div v-if="!success">
          <div v-if="error" class="bg-red-100 border-2 border-red-400 p-3 text-sm font-bold text-red-700 mb-4">
            {{ error }}
          </div>

          <form @submit.prevent="resetPassword" class="space-y-4">
            <div>
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Token</label>
              <input
                v-model="token"
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm font-mono"
                placeholder="Token de recuperacion"
                required
              />
            </div>
            <div>
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Nueva contrasena</label>
              <input
                v-model="newPassword"
                type="password"
                minlength="8"
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                placeholder="Minimo 8 caracteres"
                required
              />
            </div>
            <div>
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Confirmar contrasena</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                placeholder="Repite la contrasena"
                required
              />
            </div>
            <button
              type="submit"
              class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 w-full uppercase tracking-wide disabled:opacity-60"
              :disabled="loading || !token || !newPassword || !confirmPassword"
            >
              {{ loading ? 'Restableciendo...' : 'Restablecer contrasena' }}
            </button>
          </form>
        </div>

        <div v-else class="text-center space-y-4">
          <CheckCircle2 :size="48" :stroke-width="2" class="mx-auto text-green-600" />
          <p class="font-black text-lg uppercase">Contrasena actualizada</p>
          <p class="text-brutal-black/60 text-sm">Ya puedes iniciar sesion con tu nueva contrasena.</p>
          <router-link
            to="/login"
            class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide"
          >
            Ir al login
          </router-link>
        </div>

        <div class="mt-6 text-center">
          <router-link to="/login" class="text-sm font-bold underline text-brutal-black/60 flex items-center justify-center gap-1">
            <ArrowLeft :size="14" :stroke-width="2.5" />
            Volver al login
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>
