<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Mail, ArrowLeft, CheckCircle2 } from '@lucide/vue'

import { passwordResetApi } from '../api/passwordReset'

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
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh] flex items-center">
    <div class="max-w-md mx-auto px-4 sm:px-6 w-full">
      <div class="brutal-card p-8">
        <div class="text-center mb-6">
          <span class="bg-brutal-yellow p-3 brutal-border inline-block mb-4">
            <Mail :size="24" :stroke-width="2.5" />
          </span>
          <h1 class="font-black text-2xl uppercase">Recuperar contrasena</h1>
          <p class="text-brutal-black/60 text-sm mt-2">
            Ingresa tu email y te enviaremos un token para restablecer tu contrasena.
          </p>
        </div>

        <div v-if="!sent">
          <div v-if="error" class="bg-red-100 border-2 border-red-400 p-3 text-sm font-bold text-red-700 mb-4">
            {{ error }}
          </div>

          <form @submit.prevent="requestReset" class="space-y-4">
            <div>
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Email</label>
              <input
                v-model="email"
                type="email"
                required
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                placeholder="tu@email.com"
              />
            </div>
            <button
              type="submit"
              class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 w-full uppercase tracking-wide disabled:opacity-60"
              :disabled="loading || !email"
            >
              {{ loading ? 'Enviando...' : 'Enviar token' }}
            </button>
          </form>
        </div>

        <div v-else class="text-center space-y-4">
          <CheckCircle2 :size="48" :stroke-width="2" class="mx-auto text-green-600" />
          <p class="font-bold">Token enviado.</p>
          <div v-if="token" class="bg-brutal-gray brutal-border p-3 text-sm">
            <p class="text-brutal-black/60 mb-1">Token de prueba:</p>
            <code class="font-mono font-bold text-xs break-all">{{ token }}</code>
          </div>
          <router-link
            :to="{ name: 'reset-password', query: { token } }"
            class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide"
          >
            Restablecer contrasena
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
