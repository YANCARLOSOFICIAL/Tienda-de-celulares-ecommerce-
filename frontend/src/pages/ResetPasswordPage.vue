<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Check } from '@lucide/vue'

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
    error.value = 'Las contraseñas no coinciden'
    return
  }
  loading.value = true
  error.value = null
  try {
    await passwordResetApi.confirmPassword(token.value, newPassword.value)
    success.value = true
  } catch (e: any) {
    error.value = e.message || 'Error al restablecer la contraseña'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="page">
    <div class="auth-card">
      <p class="eyebrow">Seguridad</p>
      <h1 class="page-title">Nueva contraseña</h1>

      <div v-if="!success">
        <p v-if="error" class="form-error mt-6">
          {{ error }}
        </p>

        <form @submit.prevent="resetPassword" class="auth-form">
          <div>
            <label class="field-label">Token</label>
            <input
              v-model="token"
              class="maison-input token-input"
              placeholder="Token de recuperación"
              required
            />
          </div>
          <div>
            <label class="field-label">Nueva contraseña</label>
            <input
              v-model="newPassword"
              type="password"
              minlength="8"
              class="maison-input"
              placeholder="Mínimo 8 caracteres"
              required
            />
          </div>
          <div>
            <label class="field-label">Confirmar contraseña</label>
            <input
              v-model="confirmPassword"
              type="password"
              class="maison-input"
              placeholder="Repite la contraseña"
              required
            />
          </div>
          <button
            type="submit"
            class="btn-fill w-full"
            :disabled="loading || !token || !newPassword || !confirmPassword"
          >
            {{ loading ? 'Restableciendo...' : 'Restablecer contraseña' }}
          </button>
        </form>
      </div>

      <div v-else class="success-block">
        <div class="success-icon">
          <Check :size="22" :stroke-width="2" />
        </div>
        <p class="success-title">Contraseña actualizada</p>
        <p class="success-sub">Ya puedes iniciar sesión con tu nueva contraseña.</p>
        <router-link to="/login" class="btn-fill">
          Ir al login
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

.auth-form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.token-input {
  font-family: var(--font-family-mono);
  font-size: 13px;
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
  gap: 14px;
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
  font-size: 1.25rem;
  color: var(--color-text);
}

.success-sub {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.auth-back {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: center;
}
</style>
