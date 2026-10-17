<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowRight } from '@lucide/vue'

import { useAuthStore } from '@/stores/auth'

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
  <section class="page auth-page">
    <div class="auth-shell">
      <div class="auth-aside" aria-hidden="true">
        <div class="auth-aside-overlay"></div>
        <div class="auth-aside-content">
          <p class="eyebrow">Acceso privado</p>
          <h2 class="text-display auth-aside-title">
            Su cuenta en la<br /><span class="text-gold-gradient">Maison</span>
          </h2>
          <p class="auth-aside-text">
            Pedidos, favoritos y asesoría personalizada en un solo lugar.
          </p>
        </div>
      </div>

      <div class="auth-panel">
        <p class="eyebrow">Bienvenido de vuelta</p>
        <h1 class="page-title">Iniciar sesión</h1>
        <p class="auth-sub">Accede a tu cuenta para comprar y consultar tus pedidos.</p>

        <form class="auth-form" @submit.prevent="submit">
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
          <div class="field">
            <label for="password" class="field-label">Contraseña</label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              placeholder="••••••••"
              class="maison-input"
            />
          </div>

          <p v-if="authStore.error" class="form-error">
            {{ authStore.error }}
          </p>

          <button
            type="submit"
            :disabled="authStore.loading"
            class="btn-fill w-full"
          >
            {{ authStore.loading ? 'Entrando...' : 'Entrar' }}
            <ArrowRight :size="16" :stroke-width="2" />
          </button>
        </form>

        <div class="auth-foot">
          <router-link to="/forgot-password" class="auth-link">
            ¿Olvidaste tu contraseña?
          </router-link>
          <p class="auth-note">
            ¿No tienes cuenta?
            <router-link to="/register" class="auth-link">Regístrate aquí</router-link>
          </p>
        </div>
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
    grid-template-columns: 1fr 1fr;
    min-height: 560px;
  }
}

.auth-aside {
  position: relative;
  display: none;
  background:
    linear-gradient(rgba(10, 9, 6, 0.55), rgba(10, 9, 6, 0.78)),
    url('https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=900&q=70') center/cover;
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
  max-width: 320px;
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
  margin-top: 32px;
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

.auth-foot {
  margin-top: 28px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

.auth-link {
  font-size: 13px;
  color: var(--color-accent);
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.auth-link:hover {
  opacity: 0.75;
}

.auth-note {
  font-size: 13px;
  color: var(--color-text-secondary);
}
</style>
