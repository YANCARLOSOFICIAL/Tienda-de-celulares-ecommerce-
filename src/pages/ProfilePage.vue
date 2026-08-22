<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Save, CheckCircle2 } from '@lucide/vue'

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
  <section class="py-10 sm:py-16 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center gap-3 mb-8">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <User :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Mi perfil</h1>
      </div>

      <div class="brutal-card p-6 sm:p-8 mb-6">
        <h2 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
          <User :size="18" :stroke-width="2.5" />
          Datos personales
        </h2>

        <div v-if="successMsg" class="bg-green-100 border-4 border-brutal-black p-3 font-bold text-sm mb-4 flex items-center gap-2">
          <CheckCircle2 :size="18" :stroke-width="2.5" class="text-green-600" />
          {{ successMsg }}
        </div>
        <div v-if="error" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm mb-4">
          {{ error }}
        </div>

        <form @submit.prevent="saveProfile" class="space-y-4">
          <div>
            <label class="block text-sm font-bold mb-1">Nombre completo</label>
            <input v-model="fullName" type="text" required class="w-full px-4 py-3 brutal-border bg-brutal-white font-semibold focus:outline-none focus:bg-brutal-yellow/20 transition-colors" />
          </div>
          <div>
            <label class="block text-sm font-bold mb-1">Email</label>
            <input :value="email" type="email" disabled class="w-full px-4 py-3 brutal-border bg-brutal-gray font-semibold text-brutal-black/50 cursor-not-allowed" />
            <p class="text-xs text-brutal-black/40 mt-1">El email no se puede cambiar.</p>
          </div>
          <div>
            <label class="block text-sm font-bold mb-1">Rol</label>
            <input :value="authStore.user?.role?.name" type="text" disabled class="w-full px-4 py-3 brutal-border bg-brutal-gray font-semibold text-brutal-black/50 cursor-not-allowed" />
          </div>
          <button
            type="submit"
            class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 flex items-center gap-2 uppercase tracking-wide disabled:opacity-60"
            :disabled="saving"
          >
            <Save :size="18" :stroke-width="2.5" />
            {{ saving ? 'Guardando...' : 'Guardar cambios' }}
          </button>
        </form>
      </div>

      <div class="brutal-card p-6 sm:p-8">
        <h2 class="font-black text-lg uppercase mb-4 flex items-center gap-2">
          <Lock :size="18" :stroke-width="2.5" />
          Cambiar contrasena
        </h2>

        <div v-if="passwordSuccess" class="bg-green-100 border-4 border-brutal-black p-3 font-bold text-sm mb-4 flex items-center gap-2">
          <CheckCircle2 :size="18" :stroke-width="2.5" class="text-green-600" />
          {{ passwordSuccess }}
        </div>
        <div v-if="passwordError" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm mb-4">
          {{ passwordError }}
        </div>

        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-bold mb-1">Nueva contrasena</label>
            <input v-model="newPassword" type="password" required minlength="6" class="w-full px-4 py-3 brutal-border bg-brutal-white font-semibold focus:outline-none focus:bg-brutal-yellow/20 transition-colors" placeholder="Minimo 6 caracteres" />
          </div>
          <div>
            <label class="block text-sm font-bold mb-1">Confirmar contrasena</label>
            <input v-model="confirmPassword" type="password" required minlength="6" class="w-full px-4 py-3 brutal-border bg-brutal-white font-semibold focus:outline-none focus:bg-brutal-yellow/20 transition-colors" placeholder="Repite la contrasena" />
          </div>
          <button
            type="submit"
            class="brutal-button bg-brutal-black text-brutal-white px-6 py-3 flex items-center gap-2 uppercase tracking-wide disabled:opacity-60"
            :disabled="savingPassword"
          >
            <Lock :size="18" :stroke-width="2.5" />
            {{ savingPassword ? 'Actualizando...' : 'Cambiar contrasena' }}
          </button>
        </form>
      </div>
    </div>
  </section>
</template>
