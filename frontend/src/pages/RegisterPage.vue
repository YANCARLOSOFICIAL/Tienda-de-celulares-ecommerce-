<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight } from '@lucide/vue'

import { useAuthStore } from '@/stores/auth'

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
  <section class="page auth-page">
    <div class="auth-shell">
      <div class="auth-aside" aria-hidden="true">
        <div class="auth-aside-content">
          <p class="eyebrow">Inner Circle</p>
          <h2 class="text-display auth-aside-title">
            Únase a la<br /><span class="text-gold-gradient">Maison</span>
          </h2>
          <p class="auth-aside-text">
            Acceso anticipado a lanzamientos, canje y asesoría privada.
          </p>
        </div>
      </div>

      <div class="auth-panel">
        <p class="eyebrow">Nueva membresía</p>
        <h1 class="page-title">Crear cuenta</h1>
        <p class="auth-sub">Regístrate para comprar en Tienda Cell.</p>

        <form class="auth-form" @submit.prevent="submit">
          <div class="field">
            <label for="full_name" class="field-label">Nombre completo</label>
            <input
              id="full_name"
              v-model="fullName"
              type="text"
              required
              autocomplete="name"
              placeholder="Tu nombre"
              class="maison-input"
            />
          </div>
          <div class="field">
            <label for="email" class="field-label">Correo electrónico</label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              autocomplete="email"
              placeholder="tu@correo.com"
              class="maison-input"
            />
          </div>
          <div class="field-row">
            <div class="field">
              <label for="password" class="field-label">Contraseña</label>
              <input
                id="password"
                v-model="password"
                type="password"
                required
                autocomplete="new-password"
                placeholder="Mínimo 8 caracteres"
                class="maison-input"
              />
            </div>
            <div class="field">
              <label for="confirm_password" class="field-label">Confirmar contraseña</label>
              <input
                id="confirm_password"
                v-model="confirmPassword"
                type="password"
                required
                autocomplete="new-password"
                placeholder="Repite tu contraseña"
                class="maison-input"
              />
            </div>
          </div>

          <p v-if="formError" class="form-error">
            {{ formError }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-fill w-full"
          >
            {{ authStore.loading ? 'Creando...' : 'Crear cuenta' }}
            <ArrowRight :size="16" :stroke-width="2" />
          </button>
        </form>

        <p class="auth-foot-note">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="auth-link">Inicia sesión</router-link>
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
}

.auth-shell {
  width: 100%;
  max-width: 1040px;
  margin: 0 auto;
  display: grid;
  border: 1px solid var(--color-border);
}

@media (min-width: 900px) {
  .auth-shell {
    grid-template-columns: 1fr 1.2fr;
    min-height: 560px;
  }
}

.auth-aside {
  position: relative;
  display: none;
  background:
    linear-gradient(rgba(10, 9, 6, 0.55), rgba(10, 9, 6, 0.8)),
    url('https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=900&q=70') center/cover;
}

@media (min-width: 900px) {
  .auth-aside {
    display: flex;
    align-items: flex-end;
  }
}

.auth-aside-content {
  position: relative;
  z-index: 2;
  padding: 48px;
}

.auth-aside-title {
  font-size: clamp(1.9rem, 3vw, 2.6rem);
  margin-top: 14px;
}

.auth-aside-text {
  margin-top: 16px;
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-secondary);
  max-width: 300px;
}

.auth-panel {
  padding: clamp(2rem, 5vw, 3.5rem);
  background: var(--color-surface-dim);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.auth-sub {
  margin-top: 12px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.auth-form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-row {
  display: grid;
  gap: 16px;
}

@media (min-width: 560px) {
  .field-row {
    grid-template-columns: 1fr 1fr;
  }
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

.auth-foot-note {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
  text-align: center;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.auth-link {
  color: var(--color-accent);
  text-decoration: none;
}

.auth-link:hover {
  opacity: 0.75;
}
</style>
