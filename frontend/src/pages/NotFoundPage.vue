<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Home, ArrowLeft, Compass } from '@lucide/vue'

const router = useRouter()
const query = ref('')

function search() {
  const q = query.value.trim()
  router.push(q ? { name: 'shop', query: { search: q } } : { name: 'shop' })
}
</script>

<template>
  <section class="section-clean min-h-[70vh] flex items-center">
    <div class="max-w-lg mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="w-16 h-16 mx-auto mb-6 rounded-2xl bg-surface-dim flex items-center justify-center">
        <Compass :size="30" :stroke-width="1.5" class="text-text-tertiary" />
      </div>

      <p class="eyebrow justify-center mb-3">Error 404</p>
      <h1 class="section-title mb-3">Esta página no existe</h1>
      <p class="section-subtitle mx-auto mb-8">
        Puede que el enlace esté roto o que el producto ya no esté disponible.
        Busca lo que necesitas o vuelve al inicio.
      </p>

      <form class="flex gap-2 mb-6" @submit.prevent="search">
        <div class="relative flex-1">
          <Search :size="16" class="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" />
          <input
            v-model="query"
            type="search"
            placeholder="Buscar productos..."
            aria-label="Buscar productos"
            class="input-minimal w-full pl-10 pr-4"
          />
        </div>
        <button type="submit" class="btn-gold px-5 rounded-full text-sm font-semibold whitespace-nowrap">
          Buscar
        </button>
      </form>

      <div class="flex items-center justify-center gap-3">
        <button
          class="btn-secondary flex items-center gap-2 text-sm"
          @click="router.back()"
        >
          <ArrowLeft :size="16" :stroke-width="2" />
          Volver
        </button>
        <router-link to="/" class="btn-primary text-sm">
          <Home :size="16" :stroke-width="2" />
          Ir al inicio
        </router-link>
      </div>
    </div>
  </section>
</template>
