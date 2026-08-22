<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Save, Lock, CheckCircle2 } from '@lucide/vue'

import { authApi } from '../api/auth'
import { useAuthStore } from '../stores/auth'
import { ApiError } from '../api/client'

const router = useRouter()
const authStore = useAuthStore()

const fullName = ref('')
const email = ref('')
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const saving = ref(false)
const savingPassword = ref(false)
const successMsg = ref<string | null>(null)
const passwordSuccess = ref<string | null>(null)
const error = ref<string | null>(null)
const passwordError = ref<string | null>(null)

const initials = computed(() => {
  const parts = fullName.value.trim().split(/\s+/)
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  return fullName.value.slice(0, 2).toUpperCase() || 'U'
})

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/profile' } })
    return
  }
  await authStore.fetchMe()
  fullName.value = authStore.user?.full_name || ''
  email.value = authStore.user?.email || ''
})

async function saveProfile() {
  saving.value = true
  error.value = null
  successMsg.value = null
  try {
    await authApi.updateProfile({ full_name: fullName.value })
    await authStore.fetchMe()
    successMsg.value = 'Perfil actualizado correctamente.'
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Error al actualizar perfil.'
  } finally {
    saving.value = false
  }
}

async function changePassword() {
  if (newPassword.value !== confirmPassword.value) {
    passwordError.value = 'Las contrasenas no coinciden.'
    return
  }
  if (newPassword.value.length < 6) {
    passwordError.value = 'La contrasena debe tener al menos 6 caracteres.'
    return
  }
  savingPassword.value = true
  passwordError.value = null
  passwordSuccess.value = null
  try {
    await authApi.updateProfile({ password: newPassword.value })
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    passwordSuccess.value = 'Contrasena actualizada correctamente.'
  } catch (e) {
    passwordError.value = e instanceof ApiError ? e.message : 'Error al cambiar contrasena.'
  } finally {
    savingPassword.value = false
  }
}
</script>

<template>
  <section class="py-10 sm:py-16 min-h-[70vh]">
    <div class="max-w-4xl mx-auto px-4 sm:px-6">
      <div class="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
        <div class="bg-surface-dim border border-border rounded-2xl p-8 flex flex-col items-center text-center hover:border-white/10 transition-colors">
          <div class="w-24 h-24 rounded-full bg-gold/10 flex items-center justify-center mb-4">
            <span class="text-2xl font-semibold text-gold">{{ initials }}</span>
          </div>
          <h1 class="text-xl font-semibold tracking-tight text-white" style="font-family: var(--font-family-serif);">{{ fullName || 'Usuario' }}</h1>
          <p class="text-text-secondary text-sm mt-1">{{ email }}</p>
          <div class="mt-3 badge badge-accent">{{ authStore.user?.role?.name || 'Usuario' }}</div>
        </div>

        <div class="space-y-6">
          <div class="bg-surface-dim border border-border rounded-2xl p-6 sm:p-8 hover:border-white/10 transition-colors">
            <h2 class="text-lg font-semibold mb-4 flex items-center gap-2 text-white" style="font-family: var(--font-family-serif);">
              Datos personales
            </h2>

            <p v-if="successMsg" class="flex items-center gap-2 text-sm font-medium text-success mb-4">
              <CheckCircle2 :size="16" :stroke-width="2" />
              {{ successMsg }}
            </p>
            <p v-if="error" class="text-sm text-danger font-medium mb-4">{{ error }}</p>

            <form @submit.prevent="saveProfile" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Nombre completo</label>
                <input v-model="fullName" type="text" required class="input-minimal" />
              </div>
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Email</label>
                <input :value="email" type="email" disabled class="input-minimal opacity-60 cursor-not-allowed" />
                <p class="text-xs text-text-tertiary mt-1">El email no se puede cambiar.</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Rol</label>
                <input :value="authStore.user?.role?.name" type="text" disabled class="input-minimal opacity-60 cursor-not-allowed" />
              </div>
              <button
                type="submit"
                class="btn-gold flex items-center gap-2"
                :disabled="saving"
              >
                <Save :size="18" :stroke-width="2" />
                {{ saving ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </form>
          </div>

          <div class="bg-surface-dim border border-border rounded-2xl p-6 sm:p-8 hover:border-white/10 transition-colors">
            <h2 class="text-lg font-semibold mb-4 flex items-center gap-2 text-white" style="font-family: var(--font-family-serif);">
              <Lock :size="18" :stroke-width="2" />
              Cambiar contraseña
            </h2>

            <p v-if="passwordSuccess" class="flex items-center gap-2 text-sm font-medium text-success mb-4">
              <CheckCircle2 :size="16" :stroke-width="2" />
              {{ passwordSuccess }}
            </p>
            <p v-if="passwordError" class="text-sm text-danger font-medium mb-4">{{ passwordError }}</p>

            <form @submit.prevent="changePassword" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Nueva contraseña</label>
                <input v-model="newPassword" type="password" required minlength="6" class="input-minimal" placeholder="Mínimo 6 caracteres" />
              </div>
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Confirmar contraseña</label>
                <input v-model="confirmPassword" type="password" required minlength="6" class="input-minimal" placeholder="Repite la contraseña" />
              </div>
              <button
                type="submit"
                class="btn-gold flex items-center gap-2"
                :disabled="savingPassword"
              >
                <Lock :size="18" :stroke-width="2" />
                {{ savingPassword ? 'Actualizando...' : 'Cambiar contraseña' }}
              </button>
            </form>
          </div>

          <div class="bg-surface-dim border border-border rounded-2xl p-6 sm:p-8 hover:border-white/10 transition-colors">
            <h2 class="text-lg font-semibold text-danger mb-2" style="font-family: var(--font-family-serif);">Zona de peligro</h2>
            <p class="text-text-secondary text-sm mb-4">Eliminar tu cuenta es permanente y no se puede deshacer.</p>
            <button class="border border-danger text-danger font-semibold py-2.5 px-6 rounded-full transition hover:bg-danger/5 cursor-not-allowed" disabled>
              Eliminar cuenta
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
