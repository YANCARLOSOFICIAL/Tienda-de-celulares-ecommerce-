<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FolderKanban, Pencil, Plus, Trash2, X } from '@lucide/vue'

import { categoriesApi, type Category } from '@/api/categories'

const categories = ref<Category[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const banner = ref<string | null>(null)

const editingId = ref<number | null>(null)
const showForm = ref(false)
const formName = ref('')
const formDescription = ref('')
const formBusy = ref(false)
const formError = ref<string | null>(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    categories.value = await categoriesApi.list()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar categorías.'
  } finally {
    loading.value = false
  }
}

function openNew() {
  editingId.value = null
  showForm.value = true
  formName.value = ''
  formDescription.value = ''
  formError.value = null
}

function openEdit(category: Category) {
  editingId.value = category.id
  showForm.value = true
  formName.value = category.name
  formDescription.value = category.description ?? ''
  formError.value = null
}

async function save() {
  formBusy.value = true
  formError.value = null
  try {
    if (editingId.value !== null) {
      await categoriesApi.update(editingId.value, {
        name: formName.value.trim(),
        description: formDescription.value.trim() || null,
      })
      banner.value = 'Categoría actualizada correctamente.'
    } else {
      await categoriesApi.create({
        name: formName.value.trim(),
        description: formDescription.value.trim() || null,
      })
      banner.value = 'Categoría creada correctamente.'
    }
    editingId.value = null
    showForm.value = false
    formName.value = ''
    formDescription.value = ''
    await load()
  } catch (e) {
    formError.value = e instanceof Error ? e.message : 'Error al guardar la categoría.'
  } finally {
    formBusy.value = false
  }
}

async function confirmDelete(category: Category) {
  if (!window.confirm(`¿Eliminar la categoría "${category.name}"?`)) return
  try {
    await categoriesApi.remove(category.id)
    banner.value = 'Categoría eliminada correctamente.'
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'No se pudo eliminar la categoría.'
  }
}

onMounted(load)
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-text flex items-center gap-2" style="font-family: var(--font-family-serif);">
          <FolderKanban :size="24" :stroke-width="2" />
          Categorías
        </h2>
        <p class="text-sm text-text-secondary">Organiza el catálogo. No se pueden eliminar categorías con productos asociados.</p>
      </div>
      <button class="btn-primary flex items-center gap-2 text-sm" @click="openNew">
        <Plus :size="16" :stroke-width="2" />
        Crear categoría
      </button>
    </div>

    <p v-if="banner" class="badge-success px-4 py-2 text-sm font-medium">{{ banner }}</p>
    <p v-if="error" class="badge-danger px-4 py-2 text-sm font-medium">{{ error }}</p>

    <div v-if="showForm" class="bento-card-static glass">
      <div class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-text">{{ editingId !== null ? 'Editar categoría' : 'Nueva categoría' }}</h3>
          <button class="text-text-secondary hover:text-text transition-colors p-1" aria-label="Cerrar formulario" @click="showForm = false">
            <X :size="18" :stroke-width="2" />
          </button>
        </div>
        <form class="space-y-4" @submit.prevent="save">
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Nombre *</label>
            <input v-model="formName" required class="input-minimal" placeholder="Ej: Smartphones" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Descripción</label>
            <textarea v-model="formDescription" rows="2" class="input-minimal resize-none"></textarea>
          </div>
          <p v-if="formError" class="badge-danger px-4 py-2 text-sm">{{ formError }}</p>
          <div class="flex gap-3 justify-end">
            <button type="button" class="btn-secondary text-sm" @click="showForm = false">Cancelar</button>
            <button type="submit" :disabled="formBusy" class="btn-primary text-sm disabled:opacity-50">
              {{ formBusy ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="bento-card-static glass p-5">
        <div class="flex items-start justify-between gap-2 mb-3">
          <div class="skeleton h-5 w-32"></div>
          <div class="skeleton h-5 w-16"></div>
        </div>
        <div class="skeleton h-3 w-48 mb-3"></div>
        <div class="skeleton h-4 w-20"></div>
      </div>
    </div>

    <div v-else-if="categories.length === 0" class="bento-card-static glass p-12 text-center">
      <FolderKanban :size="40" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-3" />
      <p class="text-lg font-semibold text-text">Sin categorías</p>
      <p class="text-sm text-text-secondary mt-1">Crea tu primera categoría para organizar los productos.</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="category in categories" :key="category.id" class="bento-card-static glass p-5 flex flex-col admin-card-neon">
        <div class="flex items-start justify-between gap-2 mb-2">
          <h3 class="font-semibold text-text leading-tight">{{ category.name }}</h3>
          <div class="flex gap-1 flex-shrink-0">
            <button class="p-1.5 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors" title="Editar" @click="openEdit(category)">
              <Pencil :size="14" :stroke-width="2" />
            </button>
            <button class="p-1.5 text-text-secondary hover:text-danger hover:bg-danger/10 rounded-lg transition-colors" title="Eliminar" @click="confirmDelete(category)">
              <Trash2 :size="14" :stroke-width="2" />
            </button>
          </div>
        </div>
        <p class="text-sm text-text-secondary flex-1">{{ category.description || 'Sin descripción' }}</p>
        <span class="text-xs font-mono text-text-tertiary bg-surface-dim rounded-lg px-2.5 py-1 self-start mt-3">
          /{{ category.slug }}
        </span>
      </div>
    </div>
  </div>
</template>
