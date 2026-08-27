<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, ArrowLeft, CheckCircle2 } from '@lucide/vue'

import { passwordResetApi } from '@/api/passwordReset'

const router = useRouter()

const email = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const sent = ref(false)
const token = ref<string | null>(null)

async function requestReset() {
  loading.value = true
  error.value = null
  try {
    const result = await passwordResetApi.requestReset(email.value)
    sent.value = true
    const match = result.message.match(/token de prueba: (.+?)\)/)
    if (match) token.value = match[1]
  } catch (e: any) {
    error.value = e.message || 'Error al enviar el email'
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
            <Mail :size="22" :stroke-width="2" class="text-gold" />
          </div>
          <h1 class="text-2xl font-semibold tracking-tight text-white" style="font-family: var(--font-family-serif);">Recuperar contraseña</h1>
          <p class="text-text-secondary text-sm mt-2">
            Ingresa tu email y te enviaremos un token para restablecer tu contraseña.
          </p>
        </div>

        <div v-if="!sent">
          <p v-if="error" class="text-sm text-danger font-medium mb-4">
            {{ error }}
          </p>

          <form @submit.prevent="requestReset" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Email</label>
              <input
                v-model="email"
                type="email"
                required
                class="input-minimal"
                placeholder="tu@email.com"
              />
            </div>
            <button
              type="submit"
              class="btn-gold w-full"
              :disabled="loading || !email"
            >
              {{ loading ? 'Enviando...' : 'Enviar token' }}
            </button>
          </form>
        </div>

        <div v-else class="text-center space-y-4">
          <CheckCircle2 :size="48" :stroke-width="1.5" class="mx-auto text-success" />
          <p class="font-semibold text-white">Token enviado.</p>
          <div v-if="token" class="bg-surface-dim rounded-2xl p-4">
            <p class="text-text-secondary text-sm mb-1">Token de prueba:</p>
            <code class="font-mono text-xs text-white break-all">{{ token }}</code>
          </div>
          <router-link
            :to="{ name: 'reset-password', query: { token } }"
            class="btn-gold inline-flex items-center gap-2"
          >
            Restablecer contraseña
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
