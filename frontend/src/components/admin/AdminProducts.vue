<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Pencil, Plus, Trash2, X, Package } from '@lucide/vue'

import { categoriesApi, type Category } from '@/api/categories'
import { productsApi, formatPrice, type Product, type ProductPayload } from '@/api/products'

const products = ref<Product[]>([])
const categories = ref<Category[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const banner = ref<string | null>(null)

const editingId = ref<number | null>(null)
const showForm = ref(false)
const formBusy = ref(false)
const formError = ref<string | null>(null)
interface ProductForm {
  name: string
  brand: string
  model: string
  description: string
  price: string
  stock: number
  category_id: string
  image: string
  images: string[]
  is_active: boolean
}

function blankForm(): ProductForm {
  return {
    name: '', brand: '', model: '', description: '', price: '', stock: 0,
    category_id: '', image: '', images: [], is_active: true,
  }
}

const form = ref<ProductForm>(blankForm())

function addImage() {
  form.value.images.push('')
}
function removeImage(i: number) {
  form.value.images.splice(i, 1)
}

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
  form.value = blankForm()
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
    images: [...(product.images ?? [])],
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

    const gallery = form.value.images.map((s) => s.trim()).filter(Boolean)
    payload.images = gallery
    const mainImage = form.value.image.trim() || gallery[0] || ''
    if (mainImage) payload.image = mainImage

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
        <h2 class="text-2xl font-bold text-text flex items-center gap-2" style="font-family: var(--font-family-serif);">
          <Package :size="24" :stroke-width="2" />
          Productos
        </h2>
        <p class="text-sm text-text-secondary">Crea, edita y elimina productos del catálogo.</p>
      </div>
      <button class="btn-primary flex items-center gap-2 text-sm" @click="openNew">
        <Plus :size="16" :stroke-width="2" />
        Crear producto
      </button>
    </div>

    <p v-if="banner" class="badge-success px-4 py-2 text-sm font-medium">{{ banner }}</p>
    <p v-if="error" class="badge-danger px-4 py-2 text-sm font-medium">{{ error }}</p>

    <div v-if="showForm" class="bento-card-static glass">
      <div class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-text">{{ editingId !== null ? 'Editar producto' : 'Nuevo producto' }}</h3>
          <button class="text-text-secondary hover:text-text transition-colors p-1" aria-label="Cerrar formulario" @click="showForm = false">
            <X :size="18" :stroke-width="2" />
          </button>
        </div>

        <form class="grid grid-cols-1 sm:grid-cols-2 gap-4" @submit.prevent="save">
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Nombre *</label>
            <input v-model="form.name" required class="input-minimal" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Marca *</label>
            <input v-model="form.brand" required class="input-minimal" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Modelo</label>
            <input v-model="form.model" class="input-minimal" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Precio *</label>
            <input v-model="form.price" type="number" step="0.01" min="0.01" required class="input-minimal" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Stock *</label>
            <input v-model.number="form.stock" type="number" min="0" required class="input-minimal" />
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Categoría</label>
            <select v-model="form.category_id" class="input-minimal">
              <option value="">Sin categoría</option>
              <option v-for="cat in categories" :key="cat.id" :value="String(cat.id)">{{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Imagen principal (miniatura)</label>
            <input v-model="form.image" class="input-minimal" placeholder="https://... (si se deja vacía se usa la 1ª de la galería)" />
          </div>
          <div class="sm:col-span-2">
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-sm font-medium text-text-secondary">Galería de imágenes</label>
              <button type="button" class="text-xs text-accent font-medium flex items-center gap-1 hover:opacity-70" @click="addImage">
                <Plus :size="14" :stroke-width="2" /> Agregar imagen
              </button>
            </div>
            <p v-if="!form.images.length" class="text-xs text-text-tertiary">Sin imágenes adicionales.</p>
            <div v-for="(_, i) in form.images" :key="i" class="flex gap-2 mb-2">
              <input v-model="form.images[i]" class="input-minimal flex-1" :placeholder="`Imagen ${i + 1} — https://...`" />
              <button
                type="button"
                class="p-2 text-text-secondary hover:text-danger hover:bg-danger/10 rounded-lg transition-colors shrink-0"
                aria-label="Quitar imagen"
                @click="removeImage(i)"
              >
                <Trash2 :size="16" :stroke-width="2" />
              </button>
            </div>
          </div>
          <div class="sm:col-span-2">
            <label class="block text-sm font-medium text-text-secondary mb-1.5">Descripción</label>
            <textarea v-model="form.description" rows="3" class="input-minimal resize-none"></textarea>
          </div>
          <div class="sm:col-span-2 flex items-center gap-3">
            <label class="flex items-center gap-2 text-sm font-medium text-text cursor-pointer">
              <input v-model="form.is_active" type="checkbox" class="w-4 h-4 accent-accent rounded" />
              Producto activo (visible para clientes)
            </label>
          </div>

          <p v-if="formError" class="sm:col-span-2 badge-danger px-4 py-2 text-sm">{{ formError }}</p>

          <div class="sm:col-span-2 flex gap-3 justify-end">
            <button type="button" class="btn-secondary text-sm" @click="showForm = false">
              Cancelar
            </button>
            <button type="submit" :disabled="formBusy" class="btn-primary text-sm disabled:opacity-50">
              {{ formBusy ? 'Guardando...' : editingId !== null ? 'Guardar cambios' : 'Crear producto' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="loading" class="bento-card-static glass p-8">
      <div class="space-y-4">
        <div v-for="i in 5" :key="i" class="flex items-center gap-4">
          <div class="skeleton h-10 w-10 rounded-xl flex-shrink-0"></div>
          <div class="skeleton h-4 flex-1"></div>
          <div class="skeleton h-4 w-20"></div>
          <div class="skeleton h-4 w-16"></div>
        </div>
      </div>
    </div>

    <div v-else-if="products.length === 0" class="bento-card-static glass p-12 text-center">
      <Package :size="40" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-3" />
      <p class="text-lg font-semibold text-text">Sin productos</p>
      <p class="text-sm text-text-secondary mt-1">Crea tu primer producto para comenzar.</p>
    </div>

    <div v-else class="bento-card-static glass overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border-light">
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Producto</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Precio</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Stock</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Categoría</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Estado</th>
              <th class="text-right px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id" class="border-b border-border-light last:border-b-0 admin-table-row">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3">
                  <img :src="product.image || undefined" :alt="product.name" class="w-9 h-9 rounded-lg object-cover bg-surface-dim flex-shrink-0" />
                  <div>
                    <p class="font-medium text-text">{{ product.name }}</p>
                    <p class="text-xs text-text-secondary">{{ product.brand }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3 font-semibold text-text">${{ formatPrice(product.price) }}</td>
              <td class="px-4 py-3 text-text">{{ product.stock }}</td>
              <td class="px-4 py-3 text-text-secondary">{{ categoryName(product.category_id) }}</td>
              <td class="px-4 py-3">
                <span :class="['badge text-xs', product.is_active ? 'badge-success' : 'badge']">
                  {{ product.is_active ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex gap-1 justify-end">
                  <button class="p-2 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors" title="Editar" @click="openEdit(product)">
                    <Pencil :size="16" :stroke-width="2" />
                  </button>
                  <button class="p-2 text-text-secondary hover:text-danger hover:bg-danger/10 rounded-lg transition-colors" title="Eliminar" @click="confirmDelete(product)">
                    <Trash2 :size="16" :stroke-width="2" />
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
