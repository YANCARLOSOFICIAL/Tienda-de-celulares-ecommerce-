<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Tag, Plus, Pencil, Trash2, X, ToggleLeft, ToggleRight } from '@lucide/vue'

import { couponsApi, type Coupon, type CouponPayload } from '../../api/coupons'
import { formatPrice } from '../../api/products'

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
    <div class="flex items-center justify-between">
      <h2 class="font-black text-2xl uppercase flex items-center gap-2">
        <Tag :size="24" :stroke-width="2.5" />
        Cupones de descuento
      </h2>
      <button
        class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 flex items-center gap-2 text-sm uppercase tracking-wide"
        @click="openCreate"
      >
        <Plus :size="18" :stroke-width="2.5" />
        Crear cupon
      </button>
    </div>

    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="brutal-card p-4 flex gap-4">
        <div class="skeleton h-5 w-24"></div>
        <div class="skeleton h-5 w-32"></div>
        <div class="skeleton h-5 w-16"></div>
      </div>
    </div>

    <div v-else-if="coupons.length === 0" class="brutal-card p-8 text-center">
      <Tag :size="40" :stroke-width="1.5" class="mx-auto text-brutal-black/20 mb-3" />
      <p class="font-black text-xl uppercase">Sin cupones</p>
      <p class="text-brutal-black/50 mt-1">Crea tu primer cupon de descuento.</p>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b-4 border-brutal-black">
            <th class="text-left py-2 font-black uppercase">Codigo</th>
            <th class="text-left py-2 font-black uppercase">Tipo</th>
            <th class="text-left py-2 font-black uppercase">Descuento</th>
            <th class="text-left py-2 font-black uppercase">Min. compra</th>
            <th class="text-left py-2 font-black uppercase">Usos</th>
            <th class="text-left py-2 font-black uppercase">Expira</th>
            <th class="text-left py-2 font-black uppercase">Estado</th>
            <th class="text-right py-2 font-black uppercase">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="coupon in coupons" :key="coupon.id" class="border-b-2 border-brutal-black/10">
            <td class="py-3 font-black">{{ coupon.code }}</td>
            <td class="py-3">
              <span class="text-xs font-bold uppercase bg-brutal-gray px-2 py-1 brutal-border">
                {{ coupon.discount_type === 'PERCENTAGE' ? 'Porcentaje' : 'Fijo' }}
              </span>
            </td>
            <td class="py-3 font-black">{{ couponLabel(coupon) }}</td>
            <td class="py-3">${{ formatPrice(coupon.min_purchase) }}</td>
            <td class="py-3">
              {{ coupon.used_count }}{{ coupon.max_uses ? ` / ${coupon.max_uses}` : '' }}
            </td>
            <td class="py-3 text-brutal-black/60">
              {{ coupon.expires_at ? new Date(coupon.expires_at).toLocaleDateString('es-MX') : 'Sin limite' }}
            </td>
            <td class="py-3">
              <span
                v-if="isExpired(coupon)"
                class="text-xs font-bold uppercase bg-red-100 text-red-600 px-2 py-1 brutal-border"
              >
                Expirado
              </span>
              <span
                v-else-if="isMaxedOut(coupon)"
                class="text-xs font-bold uppercase bg-orange-100 text-orange-600 px-2 py-1 brutal-border"
              >
                Agotado
              </span>
              <span
                v-else-if="coupon.is_active"
                class="text-xs font-bold uppercase bg-green-100 text-green-700 px-2 py-1 brutal-border"
              >
                Activo
              </span>
              <span v-else class="text-xs font-bold uppercase bg-brutal-gray px-2 py-1 brutal-border">
                Inactivo
              </span>
            </td>
            <td class="py-3">
              <div class="flex items-center justify-end gap-1">
                <button
                  class="p-2 hover:bg-brutal-gray transition-colors"
                  :title="coupon.is_active ? 'Desactivar' : 'Activar'"
                  @click="toggleActive(coupon)"
                >
                  <ToggleRight v-if="coupon.is_active" :size="18" :stroke-width="2.5" class="text-green-600" />
                  <ToggleLeft v-else :size="18" :stroke-width="2.5" class="text-brutal-black/40" />
                </button>
                <button
                  class="p-2 hover:bg-brutal-gray transition-colors"
                  title="Editar"
                  @click="openEdit(coupon)"
                >
                  <Pencil :size="18" :stroke-width="2.5" />
                </button>
                <button
                  class="p-2 hover:bg-red-100 text-red-600 transition-colors"
                  title="Eliminar"
                  @click="deleteCoupon(coupon)"
                >
                  <Trash2 :size="18" :stroke-width="2.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <div class="absolute inset-0 bg-brutal-black/50" @click="showModal = false"></div>
        <div class="relative bg-brutal-white brutal-border brutal-shadow p-6 w-full max-w-md space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="font-black text-xl uppercase">
              {{ editingId ? 'Editar cupon' : 'Crear cupon' }}
            </h3>
            <button class="p-1 hover:bg-brutal-gray" @click="showModal = false">
              <X :size="20" :stroke-width="2.5" />
            </button>
          </div>

          <div v-if="formError" class="bg-red-100 border-2 border-red-400 p-3 text-sm font-bold text-red-700">
            {{ formError }}
          </div>

          <div class="space-y-3">
            <div v-if="!editingId">
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Codigo *</label>
              <input
                v-model="form.code"
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm uppercase"
                placeholder="Ej: VERANO20"
                maxlength="50"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Tipo *</label>
                <select
                  v-model="form.discount_type"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                >
                  <option v-for="dt in discountTypes" :key="dt.value" :value="dt.value">
                    {{ dt.label }}
                  </option>
                </select>
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">
                  {{ form.discount_type === 'PERCENTAGE' ? 'Porcentaje *' : 'Monto *' }}
                </label>
                <input
                  v-model.number="form.discount_value"
                  type="number"
                  :min="form.discount_type === 'PERCENTAGE' ? 1 : 0.01"
                  :max="form.discount_type === 'PERCENTAGE' ? 100 : undefined"
                  step="0.01"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Compra minima ($)</label>
                <input
                  v-model.number="form.min_purchase"
                  type="number"
                  min="0"
                  step="0.01"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Max. usos</label>
                <input
                  v-model.number="form.max_uses"
                  type="number"
                  min="1"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                  placeholder="Sin limite"
                />
              </div>
            </div>

            <div>
              <label class="font-bold text-xs uppercase tracking-wide block mb-1">Expira</label>
              <input
                v-model="form.expires_at"
                type="datetime-local"
                class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
              />
            </div>
          </div>

          <div class="flex justify-end gap-2 pt-2">
            <button
              class="brutal-button bg-brutal-white text-brutal-black px-4 py-2 text-sm uppercase tracking-wide"
              @click="showModal = false"
            >
              Cancelar
            </button>
            <button
              class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 text-sm uppercase tracking-wide disabled:opacity-60"
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
