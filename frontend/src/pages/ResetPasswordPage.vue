<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Lock, ArrowLeft, CheckCircle2 } from '@lucide/vue'

import { passwordResetApi } from '@/api/passwordReset'

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
  <section class="py-16 sm:py-24 min-h-[70vh] flex items-center">
    <div class="max-w-md mx-auto px-4 w-full">
      <div class="bg-surface-dim border border-border rounded-2xl p-8">
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gold/10 mb-4">
            <Lock :size="22" :stroke-width="2" class="text-gold" />
          </div>
          <h1 class="text-2xl font-semibold tracking-tight text-white" style="font-family: var(--font-family-serif);">Nueva contraseña</h1>
        </div>

        <div v-if="!success">
          <p v-if="error" class="text-sm text-danger font-medium mb-4">
            {{ error }}
          </p>

          <form @submit.prevent="resetPassword" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Token</label>
              <input
                v-model="token"
                class="input-minimal font-mono text-sm"
                placeholder="Token de recuperacion"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Nueva contraseña</label>
              <input
                v-model="newPassword"
                type="password"
                minlength="8"
                class="input-minimal"
                placeholder="Mínimo 8 caracteres"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Confirmar contraseña</label>
              <input
                v-model="confirmPassword"
                type="password"
                class="input-minimal"
                placeholder="Repite la contraseña"
                required
              />
            </div>
            <button
              type="submit"
              class="btn-gold w-full"
              :disabled="loading || !token || !newPassword || !confirmPassword"
            >
              {{ loading ? 'Restableciendo...' : 'Restablecer contraseña' }}
            </button>
          </form>
        </div>

        <div v-else class="text-center space-y-4">
          <CheckCircle2 :size="48" :stroke-width="1.5" class="mx-auto text-success" />
          <p class="text-lg font-semibold text-white">Contraseña actualizada</p>
          <p class="text-text-secondary text-sm">Ya puedes iniciar sesión con tu nueva contraseña.</p>
          <router-link
            to="/login"
            class="btn-gold inline-flex items-center gap-2"
          >
            Ir al login
          </router-link>
        </div>

        <div class="mt-6 text-center">
          <router-link to="/login" class="btn-ghost text-sm inline-flex items-center gap-1">
            <ArrowLeft :size="14" :stroke-width="2" />
            Volver al login
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>
