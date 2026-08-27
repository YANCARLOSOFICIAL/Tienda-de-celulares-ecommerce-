<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Tag, Plus, Pencil, Trash2, X } from '@lucide/vue'

import { couponsApi, type Coupon, type CouponPayload } from '@/api/coupons'
import { formatPrice } from '@/api/products'

const coupons = ref<Coupon[]>([])
const loading = ref(true)
const showModal = ref(false)
const editingId = ref<number | null>(null)
const saving = ref(false)
const formError = ref<string | null>(null)

const form = ref<CouponPayload>({
  code: '',
  discount_type: 'PERCENTAGE',
  discount_value: 10,
  min_purchase: 0,
  max_uses: null,
  expires_at: null,
})

const discountTypes = [
  { value: 'PERCENTAGE', label: 'Porcentaje (%)' },
  { value: 'FIXED', label: 'Monto fijo ($)' },
]

onMounted(fetchCoupons)

async function fetchCoupons() {
  loading.value = true
  try {
    coupons.value = await couponsApi.list()
  } catch {
    coupons.value = []
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = { code: '', discount_type: 'PERCENTAGE', discount_value: 10, min_purchase: 0, max_uses: null, expires_at: null }
  formError.value = null
  showModal.value = true
}

function openEdit(coupon: Coupon) {
  editingId.value = coupon.id
  form.value = {
    code: coupon.code,
    discount_type: coupon.discount_type as 'PERCENTAGE' | 'FIXED',
    discount_value: Number(coupon.discount_value),
    min_purchase: Number(coupon.min_purchase),
    max_uses: coupon.max_uses,
    expires_at: coupon.expires_at ? coupon.expires_at.slice(0, 16) : null,
  }
  formError.value = null
  showModal.value = true
}

async function saveCoupon() {
  saving.value = true
  formError.value = null
  try {
    if (editingId.value) {
      await couponsApi.update(editingId.value, { ...form.value, code: undefined })
    } else {
      await couponsApi.create(form.value)
    }
    showModal.value = false
    await fetchCoupons()
  } catch (e: any) {
    formError.value = e.message || 'Error al guardar el cupon'
  } finally {
    saving.value = false
  }
}

async function toggleActive(coupon: Coupon) {
  await couponsApi.update(coupon.id, { is_active: !coupon.is_active })
  await fetchCoupons()
}

async function deleteCoupon(coupon: Coupon) {
  if (!confirm(`Eliminar el cupon "${coupon.code}"?`)) return
  await couponsApi.remove(coupon.id)
  await fetchCoupons()
}

function isExpired(coupon: Coupon): boolean {
  if (!coupon.expires_at) return false
  return new Date(coupon.expires_at) < new Date()
}

function isMaxedOut(coupon: Coupon): boolean {
  return coupon.max_uses !== null && coupon.used_count >= coupon.max_uses
}

function couponLabel(coupon: Coupon): string {
  if (coupon.discount_type === 'PERCENTAGE') return `${coupon.discount_value}%`
  return `$${formatPrice(coupon.discount_value)}`
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h2 class="text-2xl font-bold text-text flex items-center gap-2" style="font-family: var(--font-family-serif);">
          <Tag :size="24" :stroke-width="2" />
          Cupones de descuento
        </h2>
        <p class="text-sm text-text-secondary">Gestiona cupones de descuento para tu tienda.</p>
      </div>
      <button class="btn-primary flex items-center gap-2 text-sm" @click="openCreate">
        <Plus :size="16" :stroke-width="2" />
        Crear cupón
      </button>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="bento-card-static glass p-4">
        <div class="flex gap-4">
          <div class="skeleton h-5 w-24"></div>
          <div class="skeleton h-5 w-32"></div>
          <div class="skeleton h-5 w-16"></div>
        </div>
      </div>
    </div>

    <div v-else-if="coupons.length === 0" class="bento-card-static glass p-12 text-center">
      <Tag :size="40" :stroke-width="1.5" class="mx-auto text-text-tertiary mb-3" />
      <p class="text-lg font-semibold text-text">Sin cupones</p>
      <p class="text-sm text-text-secondary mt-1">Crea tu primer cupón de descuento.</p>
    </div>

    <div v-else class="bento-card-static glass overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-border-light">
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Código</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Tipo</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Descuento</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Min. compra</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Usos</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Expira</th>
              <th class="text-left px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Estado</th>
              <th class="text-right px-4 py-3 text-xs font-medium text-text-secondary uppercase tracking-wider">Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="coupon in coupons" :key="coupon.id" class="border-b border-border-light last:border-b-0 admin-table-row">
              <td class="px-4 py-3 font-mono font-semibold text-text">{{ coupon.code }}</td>
              <td class="px-4 py-3">
                <span class="badge text-xs">
                  {{ coupon.discount_type === 'PERCENTAGE' ? 'Porcentaje' : 'Fijo' }}
                </span>
              </td>
              <td class="px-4 py-3 font-semibold text-text">{{ couponLabel(coupon) }}</td>
              <td class="px-4 py-3 text-text-secondary">${{ formatPrice(coupon.min_purchase) }}</td>
              <td class="px-4 py-3 text-text-secondary">
                {{ coupon.used_count }}{{ coupon.max_uses ? ` / ${coupon.max_uses}` : '' }}
              </td>
              <td class="px-4 py-3 text-text-secondary">
                {{ coupon.expires_at ? new Date(coupon.expires_at).toLocaleDateString('es-MX') : 'Sin límite' }}
              </td>
              <td class="px-4 py-3">
                <span v-if="isExpired(coupon)" class="badge badge-danger text-xs">
                  Expirado
                </span>
                <span v-else-if="isMaxedOut(coupon)" class="badge badge-warning text-xs">
                  Agotado
                </span>
                <span v-else-if="coupon.is_active" class="badge badge-success text-xs">
                  Activo
                </span>
                <span v-else class="badge text-xs">
                  Inactivo
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <button
                    class="p-2 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors"
                    :title="coupon.is_active ? 'Desactivar' : 'Activar'"
                    @click="toggleActive(coupon)"
                  >
                    <span class="flex items-center justify-center w-4 h-4 rounded-full border-2 transition-colors" :class="coupon.is_active ? 'border-success bg-success/20' : 'border-border'">
                      <span v-if="coupon.is_active" class="w-2 h-2 rounded-full bg-success"></span>
                    </span>
                  </button>
                  <button
                    class="p-2 text-text-secondary hover:text-accent hover:bg-accent/10 rounded-lg transition-colors"
                    title="Editar"
                    @click="openEdit(coupon)"
                  >
                    <Pencil :size="16" :stroke-width="2" />
                  </button>
                  <button
                    class="p-2 text-text-secondary hover:text-danger hover:bg-danger/10 rounded-lg transition-colors"
                    title="Eliminar"
                    @click="deleteCoupon(coupon)"
                  >
                    <Trash2 :size="16" :stroke-width="2" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showModal = false"></div>
        <div class="relative bg-surface-dim rounded-2xl border border-border shadow-xl w-full max-w-md space-y-0 overflow-hidden">
          <div class="flex items-center justify-between p-6 pb-0">
            <h3 class="text-lg font-semibold text-text">
              {{ editingId ? 'Editar cupón' : 'Crear cupón' }}
            </h3>
            <button class="text-text-secondary hover:text-text transition-colors p-1" @click="showModal = false">
              <X :size="18" :stroke-width="2" />
            </button>
          </div>

          <div v-if="formError" class="mx-6 mt-4 badge-danger px-4 py-2 text-sm">
            {{ formError }}
          </div>

          <div class="p-6 space-y-4">
            <div v-if="!editingId">
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Código *</label>
              <input
                v-model="form.code"
                class="input-minimal uppercase font-mono"
                placeholder="Ej: VERANO20"
                maxlength="50"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Tipo *</label>
                <select
                  v-model="form.discount_type"
                  class="input-minimal"
                >
                  <option v-for="dt in discountTypes" :key="dt.value" :value="dt.value">
                    {{ dt.label }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">
                  {{ form.discount_type === 'PERCENTAGE' ? 'Porcentaje *' : 'Monto *' }}
                </label>
                <input
                  v-model.number="form.discount_value"
                  type="number"
                  :min="form.discount_type === 'PERCENTAGE' ? 1 : 0.01"
                  :max="form.discount_type === 'PERCENTAGE' ? 100 : undefined"
                  step="0.01"
                  class="input-minimal"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Compra mínima ($)</label>
                <input
                  v-model.number="form.min_purchase"
                  type="number"
                  min="0"
                  step="0.01"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-text-secondary mb-1.5">Máx. usos</label>
                <input
                  v-model.number="form.max_uses"
                  type="number"
                  min="1"
                  class="input-minimal"
                  placeholder="Sin límite"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-text-secondary mb-1.5">Expira</label>
              <input
                v-model="form.expires_at"
                type="datetime-local"
                class="input-minimal"
              />
            </div>
          </div>

          <div class="flex justify-end gap-3 p-6 pt-0">
            <button
              class="btn-secondary text-sm"
              @click="showModal = false"
            >
              Cancelar
            </button>
            <button
              class="btn-primary text-sm disabled:opacity-50"
              :disabled="saving || !form.code || !form.discount_value"
              @click="saveCoupon"
            >
              {{ saving ? 'Guardando...' : editingId ? 'Actualizar' : 'Crear' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
