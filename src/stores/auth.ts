import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { authApi, type User } from '../api/auth'
import { setToken } from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => Boolean(user.value))
  const isAdmin = computed(() => user.value?.role?.name === 'ADMIN')

  async function login(email: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const data = await authApi.login(email, password)
      setToken(data.access_token)
      user.value = await authApi.me()
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Error al iniciar sesión'
      return false
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, fullName: string, password: string) {
    loading.value = true
    error.value = null
    try {
      await authApi.register({ email, full_name: fullName, password })
      return true
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Error al registrarse'
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    if (!localStorage.getItem('tiendacell_token')) {
      user.value = null
      return
    }
    loading.value = true
    try {
      user.value = await authApi.me()
    } catch {
      setToken(null)
      user.value = null
    } finally {
      loading.value = false
    }
  }

  function logout() {
    setToken(null)
    user.value = null
  }

  return { user, loading, error, isAuthenticated, isAdmin, login, register, fetchMe, logout }
})
