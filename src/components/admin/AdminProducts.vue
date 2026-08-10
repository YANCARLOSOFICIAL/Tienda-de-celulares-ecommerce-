<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ChartNoAxesCombined, Pencil, Plus, Trash2, X } from '@lucide/vue'

import { categoriesApi, type Category } from '../../api/categories'
import { productsApi, type Product, type ProductPayload } from '../../api/products'

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const banner = ref<string | null>(null)

const editingId = ref<number | null>(null)
const showForm = ref(false)
const formBusy = ref(false)
const formError = ref<string | null>(null)
const form = ref({
  name: '',
  brand: '',
  model: '',
  description: '',
  price: '',
  stock: 0,
  category_id: '',
  image: '',
  is_active: true,
})

async function load() {
  loading.value = true
  error.value = null
  try {
    products.value = (await productsApi.list({ page_size: 100, ordering: '-created_at' })).items
    categories.value = await categoriesApi.list()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar productos.'
  } finally {
    loading.value = false
  }
}

function openNew() {
  editingId.value = null
  form.value = { name: '', brand: '', model: '', description: '', price: '', stock: 0, category_id: '', image: '', is_active: true }
  formError.value = null
  showForm.value = true
}

function openEdit(product: Product) {
  editingId.value = product.id
  form.value = {
    name: product.name,
    brand: product.brand,
    model: product.model ?? '',
    description: product.description ?? '',
    price: String(Number(product.price)),
    stock: product.stock,
    category_id: product.category_id ? String(product.category_id) : '',
    image: product.image ?? '',
    is_active: product.is_active,
  }
  formError.value = null
  showForm.value = true
}

async function save() {
  formBusy.value = true
  formError.value = null
  try {
    const payload: ProductPayload = {
      name: form.value.name.trim(),
      brand: form.value.brand.trim(),
      price: form.value.price,
      stock: Number(form.value.stock),
      is_active: form.value.is_active,
    }
    if (form.value.model.trim()) payload.model = form.value.model.trim()
    if (form.value.description.trim()) payload.description = form.value.description.trim()
    if (form.value.category_id) payload.category_id = Number(form.value.category_id)
    if (form.value.image.trim()) payload.image = form.value.image.trim()

    if (editingId.value !== null) {
      await productsApi.update(editingId.value, payload)
      banner.value = 'Producto actualizado correctamente.'
    } else {
      await productsApi.create(payload)
      banner.value = 'Producto creado correctamente.'
    }
    showForm.value = false
    await load()
  } catch (e) {
    formError.value = e instanceof Error ? e.message : 'Error al guardar el producto.'
  } finally {
    formBusy.value = false
  }
}

async function confirmDelete(product: Product) {
  if (!window.confirm(`¿Eliminar "${product.name}"? Esta acción no se puede deshacer.`)) return
  try {
    await productsApi.remove(product.id)
    banner.value = 'Producto eliminado correctamente.'
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al eliminar el producto.'
  }
}

function categoryName(id: number | null): string {
  return categories.value.find((c) => c.id === id)?.name ?? '—'
}

onMounted(load)
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="font-black text-2xl uppercase flex items-center gap-2">
          <ChartNoAxesCombined :size="24" :stroke-width="2.5" />
          Gestión de productos
        </h2>
        <p class="text-brutal-black/60">Crea, edita y elimina productos del catálogo. Los inactivos no se muestran a los clientes.</p>
      </div>
      <button class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 flex items-center gap-2 uppercase text-sm" @click="openNew">
        <Plus :size="16" :stroke-width="2.5" />
        Nuevo producto
      </button>
    </div>

    <p v-if="banner" class="bg-green-100 border-4 border-brutal-black p-3 font-bold text-sm">
      {{ banner }}
    </p>
    <p v-if="error" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">
      {{ error }}
    </p>

    <div v-if="showForm" class="brutal-card p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-black text-xl uppercase">{{ editingId !== null ? 'Editar producto' : 'Nuevo producto' }}</h3>
        <button class="brutal-border p-2 hover:bg-brutal-yellow transition-colors" aria-label="Cerrar formulario" @click="showForm = false">
          <X :size="18" :stroke-width="2.5" />
        </button>
      </div>

      <form class="grid grid-cols-1 sm:grid-cols-2 gap-4" @submit.prevent="save">
        <div class="sm:col-span-2">
          <label class="block font-bold text-sm uppercase mb-1">Nombre *</label>
          <input v-model="form.name" required class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Marca *</label>
          <input v-model="form.brand" required class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Modelo</label>
          <input v-model="form.model" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Precio *</label>
          <input v-model="form.price" type="number" step="0.01" min="0.01" required class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Stock *</label>
          <input v-model.number="form.stock" type="number" min="0" required class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" />
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">Categoría</label>
          <select v-model="form.category_id" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10 bg-brutal-white">
            <option value="">Sin categoría</option>
            <option v-for="cat in categories" :key="cat.id" :value="String(cat.id)">{{ cat.name }}</option>
          </select>
        </div>
        <div>
          <label class="block font-bold text-sm uppercase mb-1">URL de imagen</label>
          <input v-model="form.image" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10" placeholder="https://..." />
        </div>
        <div class="sm:col-span-2">
          <label class="block font-bold text-sm uppercase mb-1">Descripción</label>
          <textarea v-model="form.description" rows="3" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10"></textarea>
        </div>
        <div class="sm:col-span-2 flex items-center gap-3">
          <label class="flex items-center gap-2 font-bold cursor-pointer">
            <input v-model="form.is_active" type="checkbox" class="w-5 h-5" />
            Producto activo (visible para clientes)
          </label>
        </div>

        <p v-if="formError" class="sm:col-span-2 bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">
          {{ formError }}
        </p>

        <div class="sm:col-span-2 flex gap-3 justify-end">
          <button type="button" class="brutal-button bg-brutal-white text-brutal-black px-5 py-3 uppercase text-sm" @click="showForm = false">
            Cancelar
          </button>
          <button type="submit" :disabled="formBusy" class="brutal-button bg-brutal-yellow text-brutal-black px-5 py-3 uppercase text-sm disabled:opacity-60">
            {{ formBusy ? 'Guardando...' : editingId !== null ? 'Guardar cambios' : 'Crear producto' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="loading" class="brutal-card p-8 text-center font-bold">Cargando productos...</div>

    <div v-else class="brutal-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="border-b-4 border-brutal-black bg-brutal-yellow">
              <th class="px-4 py-3 font-black uppercase text-xs">Producto</th>
              <th class="px-4 py-3 font-black uppercase text-xs">Marca</th>
              <th class="px-4 py-3 font-black uppercase text-xs">Categoría</th>
              <th class="px-4 py-3 font-black uppercase text-xs">Precio</th>
              <th class="px-4 py-3 font-black uppercase text-xs">Stock</th>
              <th class="px-4 py-3 font-black uppercase text-xs">Estado</th>
              <th class="px-4 py-3 font-black uppercase text-xs text-right">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id" class="border-b-4 border-brutal-black last:border-b-0 hover:bg-brutal-gray/50">
              <td class="px-4 py-3 font-bold">
                <div class="flex items-center gap-3">
                  <img :src="product.image || undefined" :alt="product.name" class="w-10 h-10 object-cover brutal-border flex-shrink-0" />
                  <span>{{ product.name }}</span>
                </div>
              </td>
              <td class="px-4 py-3">{{ product.brand }}</td>
              <td class="px-4 py-3">{{ categoryName(product.category_id) }}</td>
              <td class="px-4 py-3 font-black">${{ Number(product.price).toLocaleString('es-MX') }}</td>
              <td class="px-4 py-3">{{ product.stock }}</td>
              <td class="px-4 py-3">
                <span :class="['font-black text-xs uppercase px-2 py-1 brutal-border', product.is_active ? 'bg-green-100 text-green-800' : 'bg-brutal-black text-brutal-white']">
                  {{ product.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex gap-2 justify-end">
                  <button class="brutal-border p-2 hover:bg-brutal-yellow transition-colors" title="Editar" @click="openEdit(product)">
                    <Pencil :size="16" :stroke-width="2.5" />
                  </button>
                  <button class="brutal-border p-2 bg-red-100 hover:bg-red-200 transition-colors" title="Eliminar" @click="confirmDelete(product)">
                    <Trash2 :size="16" :stroke-width="2.5" class="text-red-700" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>