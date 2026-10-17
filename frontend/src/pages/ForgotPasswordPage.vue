<script setup lang="ts">
import { ref } from 'vue'
import { ArrowLeft, Check } from '@lucide/vue'

import { passwordResetApi } from '@/api/passwordReset'

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
  <section class="page">
    <div class="auth-card">
      <p class="eyebrow">Recuperación</p>
      <h1 class="page-title">Recuperar contraseña</h1>
      <p class="auth-sub">
        Ingresa tu email y te enviaremos un token para restablecer tu contraseña.
      </p>

      <div v-if="!sent">
        <p v-if="error" class="form-error mt-6">
          {{ error }}
        </p>

        <form @submit.prevent="requestReset" class="auth-form">
          <div>
            <label class="field-label">Email</label>
            <input
              v-model="email"
              type="email"
              required
              class="maison-input"
              placeholder="tu@email.com"
            />
          </div>
          <button
            type="submit"
            class="btn-fill w-full"
            :disabled="loading || !email"
          >
            {{ loading ? 'Enviando...' : 'Enviar token' }}
          </button>
        </form>
      </div>

      <div v-else class="success-block">
        <div class="success-icon">
          <Check :size="22" :stroke-width="2" />
        </div>
        <p class="success-title">Token enviado.</p>
        <div v-if="token" class="token-box">
          <p class="token-label">Token de prueba:</p>
          <code class="token-value">{{ token }}</code>
        </div>
        <router-link
          :to="{ name: 'reset-password', query: { token } }"
          class="btn-fill"
        >
          Restablecer contraseña
        </router-link>
      </div>

      <div class="auth-back">
        <router-link to="/login" class="btn-ghost">
          <ArrowLeft :size="14" :stroke-width="2" />
          Volver al login
        </router-link>
      </div>
    </div>
  </section>
</template>

<style scoped>
.auth-card {
  max-width: 460px;
  margin: 0 auto;
  background: var(--color-surface-dim);
  border: 1px solid var(--color-border);
  padding: clamp(2rem, 5vw, 3rem);
}

.auth-sub {
  margin-top: 12px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
}

.auth-form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field-label {
  display: block;
  font-family: var(--font-family-mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--color-text-tertiary);
  margin-bottom: 8px;
}

.form-error {
  font-size: 13px;
  color: var(--color-danger);
}

.success-block {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.success-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.4);
  color: var(--color-success);
}

.success-title {
  font-family: var(--font-family-serif);
  font-size: 1.2rem;
  color: var(--color-text);
}

.token-box {
  width: 100%;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  padding: 14px 16px;
  text-align: left;
}

.token-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin-bottom: 6px;
}

.token-value {
  font-family: var(--font-family-mono);
  font-size: 12px;
  color: var(--color-accent);
  word-break: break-all;
}

.auth-back {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: center;
}
</style>
