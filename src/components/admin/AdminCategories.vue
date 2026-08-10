<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { FolderKanban, Pencil, Plus, Trash2 } from '@lucide/vue'

import { categoriesApi, type Category } from '../../api/categories'

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
        <h2 class="font-black text-2xl uppercase flex items-center gap-2">
          <FolderKanban :size="24" :stroke-width="2.5" />
          Gestión de categorías
        </h2>
        <p class="text-brutal-black/60">Organiza el catálogo. No se pueden eliminar categorías con productos asociados.</p>
      </div>
      <button class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 flex items-center gap-2 uppercase text-sm" @click="openNew">
        <Plus :size="16" :stroke-width="2.5" />
        Nueva categoría
      </button>
    </div>

    <p v-if="banner" class="bg-green-100 border-4 border-brutal-black p-3 font-bold text-sm">{{ banner }}</p>
    <p v-if="error" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">{{ error }}</p>

    <div v-if="showForm" class="brutal-card p-6">
      <h3 class="font-black text-xl uppercase mb-4">{{ editingId !== null ? 'Editar categoría' : 'Nueva categoría' }}</h3>
      <form class="space-y-4" @submit.prevent="save">
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Nombre *</label>
          <input v-model="formName" required class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" placeholder="Ej: Smartphones" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Descripción</label>
          <textarea v-model="formDescription" rows="2" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10"></textarea>
        </div>
        <p v-if="formError" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">{{ formError }}</p>
        <div class="flex gap-3 justify-end">
          <button type="button" class="brutal-button bg-brutal-white text-brutal-black px-5 py-2 uppercase text-sm" @click="openNew">Cancelar</button>
          <button type="submit" :disabled="formBusy" class="brutal-button bg-brutal-yellow text-brutal-black px-5 py-2 uppercase text-sm disabled:opacity-60">
            {{ formBusy ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="loading" class="brutal-card p-8 text-center font-bold">Cargando categorías...</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="category in categories" :key="category.id" class="brutal-card p-5 flex flex-col">
        <div class="flex items-start justify-between gap-2 mb-2">
          <h3 class="font-black text-lg leading-tight">{{ category.name }}</h3>
          <div class="flex gap-1 flex-shrink-0">
            <button class="brutal-border p-1.5 hover:bg-brutal-yellow transition-colors" title="Editar" @click="openEdit(category)">
              <Pencil :size="14" :stroke-width="2.5" />
            </button>
            <button class="brutal-border p-1.5 bg-red-100 hover:bg-red-200 transition-colors" title="Eliminar" @click="confirmDelete(category)">
              <Trash2 :size="14" :stroke-width="2.5" class="text-red-700" />
            </button>
          </div>
        </div>
        <p class="text-sm text-brutal-black/60 flex-1">{{ category.description || 'Sin descripción' }}</p>
        <span class="text-xs font-black uppercase bg-brutal-gray border-4 border-brutal-black px-2 py-1 self-start mt-3">
          /{{ category.slug }}
        </span>
      </div>
    </div>
  </div>
</template>