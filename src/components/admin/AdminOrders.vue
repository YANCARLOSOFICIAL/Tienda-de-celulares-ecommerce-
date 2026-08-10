<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { PackageOpen, Pencil } from '@lucide/vue'

import { ordersApi, orderStatusLabels, type Order, type OrderStatus } from '../../api/orders'

const orders = ref<Order[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const banner = ref<string | null>(null)

const editingId = ref<number | null>(null)
const editingStatus = ref<OrderStatus>('PENDING')
const formBusy = ref(false)

const statusOptions = Object.keys(orderStatusLabels) as OrderStatus[]

async function load() {
  loading.value = true
  error.value = null
  try {
    orders.value = await ordersApi.list()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al cargar pedidos.'
  } finally {
    loading.value = false
  }
}

function openEdit(order: Order) {
  editingId.value = order.id
  editingStatus.value = order.status
}

async function saveStatus() {
  if (editingId.value === null) return
  formBusy.value = true
  error.value = null
  try {
    const updated = await ordersApi.updateStatus(editingId.value, editingStatus.value)
    const idx = orders.value.findIndex((o) => o.id === updated.id)
    if (idx !== -1) orders.value[idx] = updated
    banner.value = 'Estado del pedido actualizado correctamente.'
    editingId.value = null
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Error al actualizar el estado.'
  } finally {
    formBusy.value = false
  }
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('es-MX', { dateStyle: 'short', timeStyle: 'short' })
}

onMounted(load)
</script>

<template>
  <div class="space-y-6">
    <div>
      <h2 class="font-black text-2xl uppercase flex items-center gap-2">
        <PackageOpen :size="24" :stroke-width="2.5" />
        Gestión de pedidos
      </h2>
      <p class="text-brutal-black/60">Consulta todos los pedidos y actualiza su estado.</p>
    </div>

    <p v-if="banner" class="bg-green-100 border-4 border-brutal-black p-3 font-bold text-sm">{{ banner }}</p>
    <p v-if="error" class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm">{{ error }}</p>

    <div v-if="loading" class="brutal-card p-8 text-center font-bold">Cargando pedidos...</div>

    <div v-else-if="orders.length === 0" class="brutal-card p-8 text-center font-bold text-brutal-black/60">
      No hay pedidos registrados.
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div v-for="order in orders" :key="order.id" class="brutal-card p-5">
        <div class="flex items-center justify-between gap-2 mb-2">
          <div>
            <span class="font-black text-xl">Pedido #{{ order.id }}</span>
            <p class="text-xs text-brutal-black/60 font-semibold">Usuario #{{ order.user_id }} · {{ formatDate(order.created_at) }}</p>
          </div>
          <span
            :class="[
              'font-black text-[11px] uppercase px-2 py-1 brutal-border',
              order.status === 'CANCELLED' ? 'bg-red-100 text-red-700' : 'bg-brutal-yellow text-brutal-black',
            ]"
          >
            {{ orderStatusLabels[order.status] }}
          </span>
        </div>

        <ul class="border-y-4 border-brutal-black divide-y-2 divide-brutal-black/20 my-3">
          <li v-for="item in order.items" :key="item.id" class="py-1.5 flex justify-between gap-2 text-sm font-semibold">
            <span class="truncate">{{ item.quantity }} × {{ item.product_name }}</span>
            <span class="flex-shrink-0">${{ Number(item.subtotal).toLocaleString('es-MX') }}</span>
          </li>
        </ul>

        <div class="flex items-center justify-between gap-2 mb-4">
          <span class="font-black uppercase text-xs">Total</span>
          <span class="font-black text-xl">${{ Number(order.total).toLocaleString('es-MX') }}</span>
        </div>

        <div v-if="editingId === order.id" class="space-y-2">
          <label class="block font-bold text-sm uppercase mb-1">Nuevo estado</label>
          <select v-model="editingStatus" class="w-full border-4 border-brutal-black px-3 py-2 font-semibold outline-none focus:bg-brutal-yellow/10 bg-brutal-white">
            <option v-for="status in statusOptions" :key="status" :value="status">{{ orderStatusLabels[status] }}</option>
          </select>
          <div class="flex gap-2 justify-end">
            <button class="brutal-button bg-brutal-white text-brutal-black px-4 py-2 uppercase text-xs" @click="editingId = null">
              Cancelar
            </button>
            <button :disabled="formBusy" class="brutal-button bg-brutal-yellow text-brutal-black px-4 py-2 uppercase text-xs disabled:opacity-60" @click="saveStatus">
              {{ formBusy ? 'Guardando...' : 'Guardar estado' }}
            </button>
          </div>
        </div>

        <button
          v-else
          class="w-full brutal-button bg-brutal-black text-brutal-white uppercase text-sm py-2.5 flex items-center justify-center gap-2 hover:bg-brutal-yellow hover:text-brutal-black transition-colors"
          @click="openEdit(order)"
        >
          <Pencil :size="16" :stroke-width="2.5" />
          Cambiar estado
        </button>
      </div>
    </div>
  </div>
</template>