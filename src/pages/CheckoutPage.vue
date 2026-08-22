<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  CheckCircle2,
  ShoppingBag,
  XCircle,
  MapPin,
  Truck,
  FileText,
  Plus,
  ChevronRight,
  ArrowLeft,
} from '@lucide/vue'

import { formatPrice } from '../api/products'
import { addressesApi, type Address, type AddressPayload } from '../api/addresses'
import { ordersApi, orderStatusLabels, type OrderCreatePayload } from '../api/orders'
import { couponsApi, type CouponValidateResult } from '../api/coupons'
import { paymentsApi } from '../api/payments'
import { ApiError } from '../api/client'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const step = ref<1 | 2 | 3>(1)
const processing = ref(false)
const paying = ref(false)
const showSandboxConfirm = ref(false)
const orderError = ref<string | null>(null)
const createdOrderId = ref<number | null>(null)
const createdPaymentId = ref<number | null>(null)

const addresses = ref<Address[]>([])
const selectedAddressId = ref<number | null>(null)
const showNewAddress = ref(false)

const shippingMethod = ref<string>('ESTANDAR')
const shippingCost = computed(() => {
  switch (shippingMethod.value) {
    case 'EXPRESS':
      return 199
    case 'RECOLECCION':
      return 0
    default:
      return 99
  }
})

const notes = ref('')

const couponCode = ref('')
const appliedCoupon = ref<CouponValidateResult | null>(null)
const couponError = ref<string | null>(null)
const validatingCoupon = ref(false)

const newAddress = ref<AddressPayload>({
  label: '',
  full_name: '',
  phone: '',
  street: '',
  street_number: '',
  interior: '',
  neighborhood: '',
  city: '',
  state: '',
  zip_code: '',
})

const items = computed(() => cartStore.cart?.items ?? [])
const cartTotal = computed(() => cartStore.cart?.total ?? '0')
const isEmpty = computed(() => items.value.length === 0)

const selectedAddress = computed(() =>
  addresses.value.find((a) => a.id === selectedAddressId.value) ?? null,
)

const grandTotal = computed(() => Number(cartTotal.value) + shippingCost.value - couponDiscount.value)

const couponDiscount = computed(() => {
  if (!appliedCoupon.value) return 0
  const subtotal = Number(cartTotal.value)
  if (appliedCoupon.value.discount_type === 'PERCENTAGE') {
    return Math.min(subtotal * Number(appliedCoupon.value.discount_value) / 100, subtotal)
  }
  return Math.min(Number(appliedCoupon.value.discount_value), subtotal)
})

const stepLabels = ['Direccion', 'Envio', 'Resumen']

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.replace({ name: 'login', query: { redirect: '/checkout' } })
    return
  }
  await Promise.all([cartStore.fetchCart(), fetchAddresses()])
})

async function fetchAddresses() {
  try {
    const list = await addressesApi.list()
    addresses.value = list
    const def = list.find((a) => a.is_default)
    if (def) selectedAddressId.value = def.id
    else if (list.length === 1) selectedAddressId.value = list[0].id
  } catch {
    addresses.value = []
  }
}

function goNext() {
  if (step.value < 3) step.value = (step.value + 1) as 1 | 2 | 3
}

function goBack() {
  if (step.value > 1) step.value = (step.value - 1) as 1 | 2 | 3
}

function toggleNewAddress() {
  showNewAddress.value = !showNewAddress.value
  if (showNewAddress.value) selectedAddressId.value = null
}

function selectAddress(id: number) {
  selectedAddressId.value = id
  showNewAddress.value = false
}

async function saveNewAddress() {
  try {
    const created = await addressesApi.create(newAddress.value)
    addresses.value.push(created)
    selectedAddressId.value = created.id
    showNewAddress.value = false
    resetNewAddress()
  } catch {
    orderError.value = 'No se pudo guardar la direccion.'
  }
}

function resetNewAddress() {
  newAddress.value = {
    label: '',
    full_name: '',
    phone: '',
    street: '',
    street_number: '',
    interior: '',
    neighborhood: '',
    city: '',
    state: '',
    zip_code: '',
  }
}

async function placeOrder() {
  processing.value = true
  orderError.value = null

  if (!selectedAddressId.value && !showNewAddress.value) {
    if (selectedAddress.value) {
      selectedAddressId.value = selectedAddress.value.id
    }
  }

  let addressId = selectedAddressId.value
  if (!addressId && showNewAddress.value) {
    try {
      const created = await addressesApi.create(newAddress.value)
      addressId = created.id
    } catch {
      orderError.value = 'No se pudo guardar la direccion.'
      processing.value = false
      return
    }
  }

  const payload: OrderCreatePayload = {
    address_id: addressId ?? undefined,
    shipping_method: shippingMethod.value,
    coupon_code: appliedCoupon.value ? appliedCoupon.value.code : undefined,
    notes: notes.value.trim() || undefined,
  }

  try {
    const order = await ordersApi.create(payload)
    createdOrderId.value = order.id
    await cartStore.fetchCart()
  } catch (e) {
    if (e instanceof ApiError) {
      orderError.value = e.message
    } else {
      orderError.value = 'Ocurrio un error al procesar el pedido.'
    }
  } finally {
    processing.value = false
  }
}

async function payNow() {
  if (!createdOrderId.value) return
  paying.value = true
  orderError.value = null
  try {
    const result = await paymentsApi.create(createdOrderId.value)
    createdPaymentId.value = result.payment_id
    if (result.checkout_url) {
      window.location.href = result.checkout_url
    } else {
      showSandboxConfirm.value = true
    }
  } catch (e: any) {
    orderError.value = e.message || 'Error al iniciar el pago'
  } finally {
    paying.value = false
  }
}

async function confirmSandboxPayment() {
  if (!createdPaymentId.value) return
  paying.value = true
  try {
    await paymentsApi.simulateApproval(createdPaymentId.value)
    showSandboxConfirm.value = false
    router.push({ name: 'order-detail', params: { id: createdOrderId.value } })
  } catch (e: any) {
    orderError.value = e.message || 'Error al confirmar el pago'
  } finally {
    paying.value = false
  }
}

async function applyCoupon() {
  if (!couponCode.value.trim()) return
  validatingCoupon.value = true
  couponError.value = null
  try {
    const result = await couponsApi.validate(couponCode.value.trim(), Number(cartTotal.value))
    appliedCoupon.value = result
    couponError.value = null
  } catch (e: any) {
    appliedCoupon.value = null
    couponError.value = e.message || 'Cupon invalido'
  } finally {
    validatingCoupon.value = false
  }
}

function removeCoupon() {
  appliedCoupon.value = null
  couponCode.value = ''
  couponError.value = null
}

function shipLabel(method: string) {
  switch (method) {
    case 'EXPRESS':
      return 'Express ($199)'
    case 'RECOLECCION':
      return 'Recoleccion en tienda ($0)'
    default:
      return 'Estandar ($99)'
  }
}
</script>

<template>
  <section class="py-16 sm:py-20 bg-brutal-gray min-h-[70vh]">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="flex items-center gap-3 mb-10">
        <span class="bg-brutal-yellow p-2 brutal-border flex items-center justify-center">
          <ShoppingBag :size="22" :stroke-width="2.5" class="text-brutal-black" />
        </span>
        <h1 class="font-black text-3xl sm:text-4xl uppercase">Checkout</h1>
      </div>

      <!-- SUCCESS SCREEN -->
      <div v-if="createdOrderId" class="brutal-card p-10 text-center">
        <CheckCircle2 :size="56" :stroke-width="2" class="mx-auto text-green-600 mb-4" />
        <h2 class="font-black text-2xl uppercase mb-2">Pedido creado</h2>
        <p class="text-brutal-black/70 mb-6">
          Tu pedido #{{ createdOrderId }} fue registrado con exito.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 uppercase tracking-wide flex items-center justify-center gap-2 disabled:opacity-60"
            :disabled="paying"
            @click="payNow"
          >
            {{ paying ? 'Redirigiendo...' : 'Pagar ahora' }}
          </button>
          <router-link
            to="/orders"
            class="brutal-button bg-brutal-white text-brutal-black px-6 py-3 uppercase tracking-wide"
          >
            Ver mis pedidos
          </router-link>
          <router-link
            to="/#productos"
            class="brutal-button bg-brutal-white text-brutal-black px-6 py-3 uppercase tracking-wide"
          >
            Seguir comprando
          </router-link>
        </div>
      </div>

      <!-- LOADING -->
      <div v-else-if="cartStore.loading" class="brutal-card p-10 text-center">
        <p class="font-bold text-lg">Cargando carrito...</p>
      </div>

      <!-- EMPTY CART -->
      <div v-else-if="isEmpty" class="brutal-card p-10 text-center">
        <p class="font-black text-2xl uppercase mb-4">No hay productos en tu carrito</p>
        <router-link
          to="/#productos"
          class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 inline-block uppercase tracking-wide"
        >
          Ver catalogo
        </router-link>
      </div>

      <!-- CHECKOUT FLOW -->
      <div v-else class="space-y-6">

        <!-- STEP INDICATORS -->
        <div class="flex gap-2">
          <div
            v-for="(label, i) in stepLabels"
            :key="i"
            class="flex-1 brutal-border p-3 text-center font-black text-xs sm:text-sm uppercase tracking-wide"
            :class="step === i + 1
              ? 'bg-brutal-yellow text-brutal-black'
              : step > i + 1
                ? 'bg-brutal-black text-brutal-white'
                : 'bg-brutal-white text-brutal-black/50'"
          >
            {{ i + 1 }}. {{ label }}
          </div>
        </div>

        <!-- ERROR -->
        <p
          v-if="orderError"
          class="bg-red-100 border-4 border-brutal-black p-3 font-bold text-sm flex items-center gap-2"
        >
          <XCircle :size="18" :stroke-width="2.5" />
          {{ orderError }}
        </p>

        <!-- STEP 1: ADDRESS -->
        <div v-if="step === 1" class="space-y-4">
          <div class="brutal-card p-5">
            <h2 class="font-black text-xl uppercase mb-4 flex items-center gap-2">
              <MapPin :size="20" :stroke-width="2.5" />
              Selecciona una direccion
            </h2>

            <div v-if="addresses.length === 0 && !showNewAddress" class="text-brutal-black/60 mb-4">
              No tienes direcciones guardadas.
            </div>

            <div v-else class="space-y-3 mb-4">
              <button
                v-for="addr in addresses"
                :key="addr.id"
                class="w-full text-left brutal-border p-4 cursor-pointer transition-all"
                :class="selectedAddressId === addr.id
                  ? 'bg-brutal-yellow'
                  : 'bg-brutal-white hover:bg-brutal-gray'"
                @click="selectAddress(addr.id)"
              >
                <div class="flex items-start justify-between">
                  <div class="min-w-0">
                    <p class="font-black text-sm">
                      {{ addr.label || 'Direccion' }}
                      <span v-if="addr.is_default" class="text-xs bg-brutal-black text-brutal-white px-2 py-0.5 ml-2">
                        Default
                      </span>
                    </p>
                    <p class="text-sm text-brutal-black/70 mt-1">
                      {{ addr.street }} {{ addr.street_number }}
                      <span v-if="addr.interior">, {{ addr.interior }}</span>
                    </p>
                    <p class="text-sm text-brutal-black/70">
                      {{ addr.neighborhood }}, {{ addr.city }}, {{ addr.state }} {{ addr.zip_code }}
                    </p>
                    <p class="text-xs text-brutal-black/50 mt-1">
                      {{ addr.full_name }} - {{ addr.phone }}
                    </p>
                  </div>
                  <div
                    v-if="selectedAddressId === addr.id"
                    class="w-4 h-4 brutal-border bg-brutal-black flex-shrink-0 mt-1"
                  >
                    <CheckCircle2 :size="16" class="text-brutal-white" />
                  </div>
                </div>
              </button>
            </div>

            <button
              class="brutal-button bg-brutal-white text-brutal-black px-4 py-2 flex items-center gap-2 uppercase tracking-wide text-sm"
              @click="toggleNewAddress"
            >
              <Plus :size="16" :stroke-width="2.5" />
              {{ showNewAddress ? 'Cancelar' : 'Agregar direccion nueva' }}
            </button>
          </div>

          <!-- NEW ADDRESS FORM -->
          <div v-if="showNewAddress" class="brutal-card p-5">
            <h3 class="font-black text-lg uppercase mb-4">Nueva direccion</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Etiqueta</label>
                <input
                  v-model="newAddress.label"
                  placeholder="Casa, Oficina..."
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Nombre completo *</label>
                <input
                  v-model="newAddress.full_name"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Telefono *</label>
                <input
                  v-model="newAddress.phone"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Calle *</label>
                <input
                  v-model="newAddress.street"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Numero</label>
                <input
                  v-model="newAddress.street_number"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Interior</label>
                <input
                  v-model="newAddress.interior"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Colonia *</label>
                <input
                  v-model="newAddress.neighborhood"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Ciudad *</label>
                <input
                  v-model="newAddress.city"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Estado *</label>
                <input
                  v-model="newAddress.state"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
              <div>
                <label class="font-bold text-xs uppercase tracking-wide block mb-1">Codigo postal *</label>
                <input
                  v-model="newAddress.zip_code"
                  class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm"
                />
              </div>
            </div>
            <button
              class="brutal-button bg-brutal-black text-brutal-white px-4 py-2 mt-4 flex items-center gap-2 uppercase tracking-wide text-sm"
              @click="saveNewAddress"
            >
              Guardar direccion
            </button>
          </div>

          <div class="flex justify-end">
            <button
              class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 flex items-center gap-2 uppercase tracking-wide"
              :disabled="!selectedAddressId && !showNewAddress"
              @click="goNext"
            >
              Continuar
              <ChevronRight :size="18" :stroke-width="2.5" />
            </button>
          </div>
        </div>

        <!-- STEP 2: SHIPPING METHOD -->
        <div v-if="step === 2" class="space-y-4">
          <div class="brutal-card p-5">
            <h2 class="font-black text-xl uppercase mb-4 flex items-center gap-2">
              <Truck :size="20" :stroke-width="2.5" />
              Metodo de envio
            </h2>

            <div class="space-y-3">
              <label
                v-for="method in ['ESTANDAR', 'EXPRESS', 'RECOLECCION']"
                :key="method"
                class="flex items-center gap-4 brutal-border p-4 cursor-pointer transition-all"
                :class="shippingMethod === method
                  ? 'bg-brutal-yellow'
                  : 'bg-brutal-white hover:bg-brutal-gray'"
              >
                <input
                  v-model="shippingMethod"
                  type="radio"
                  :value="method"
                  class="w-4 h-4 accent-brutal-black"
                />
                <span class="font-black text-sm uppercase tracking-wide flex-1">
                  {{ shipLabel(method) }}
                </span>
              </label>
            </div>
          </div>

          <div class="flex justify-between">
            <button
              class="brutal-button bg-brutal-white text-brutal-black px-6 py-3 flex items-center gap-2 uppercase tracking-wide"
              @click="goBack"
            >
              <ArrowLeft :size="18" :stroke-width="2.5" />
              Volver
            </button>
            <button
              class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-3 flex items-center gap-2 uppercase tracking-wide"
              @click="goNext"
            >
              Continuar
              <ChevronRight :size="18" :stroke-width="2.5" />
            </button>
          </div>
        </div>

        <!-- STEP 3: ORDER SUMMARY -->
        <div v-if="step === 3" class="space-y-4">
          <!-- Items -->
          <div class="brutal-card overflow-hidden">
            <div class="p-4 border-b-4 border-brutal-black">
              <h2 class="font-black text-xl uppercase flex items-center gap-2">
                <FileText :size="20" :stroke-width="2.5" />
                Resumen del pedido
              </h2>
            </div>
            <div
              v-for="item in items"
              :key="item.id"
              class="flex items-center justify-between gap-4 p-4 border-b-4 border-brutal-black last:border-b-0"
            >
              <div class="min-w-0">
                <h3 class="font-black leading-tight">{{ item.product.name }}</h3>
                <p class="text-sm text-brutal-black/60">
                  ${{ formatPrice(item.product.price) }} x {{ item.quantity }}
                </p>
              </div>
              <span class="font-black whitespace-nowrap">${{ formatPrice(item.subtotal) }}</span>
            </div>
          </div>

          <!-- Address & Shipping Info -->
          <div class="brutal-card p-5 space-y-3">
            <div v-if="selectedAddress" class="flex items-start gap-2">
              <MapPin :size="18" :stroke-width="2.5" class="mt-0.5 flex-shrink-0" />
              <div>
                <p class="font-black text-sm uppercase">{{ selectedAddress.label || 'Direccion' }}</p>
                <p class="text-sm text-brutal-black/70">
                  {{ selectedAddress.street }} {{ selectedAddress.street_number }}
                  <span v-if="selectedAddress.interior">, {{ selectedAddress.interior }}</span>
                </p>
                <p class="text-sm text-brutal-black/70">
                  {{ selectedAddress.neighborhood }}, {{ selectedAddress.city }}, {{ selectedAddress.state }} {{ selectedAddress.zip_code }}
                </p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <Truck :size="18" :stroke-width="2.5" />
              <span class="font-bold text-sm uppercase">{{ shipLabel(shippingMethod) }}</span>
            </div>
          </div>

          <!-- Notes -->
          <div class="brutal-card p-5">
            <label class="font-black text-sm uppercase tracking-wide block mb-2">
              Notas adicionales (opcional)
            </label>
            <textarea
              v-model="notes"
              rows="3"
              placeholder="Instrucciones de entrega, referencias..."
              class="w-full brutal-border px-3 py-2 bg-brutal-white font-bold text-sm resize-none"
            />
          </div>

          <!-- Coupon -->
          <div class="brutal-card p-5">
            <label class="font-black text-sm uppercase tracking-wide block mb-2">
              Cupon de descuento
            </label>
            <div v-if="!appliedCoupon" class="flex gap-2">
              <input
                v-model="couponCode"
                class="flex-1 brutal-border px-3 py-2 bg-brutal-white font-bold text-sm uppercase"
                placeholder="Codigo del cupon"
                @keyup.enter="applyCoupon"
              />
              <button
                class="brutal-button bg-brutal-black text-brutal-white px-4 py-2 text-sm uppercase tracking-wide disabled:opacity-60"
                :disabled="validatingCoupon || !couponCode.trim()"
                @click="applyCoupon"
              >
                {{ validatingCoupon ? 'Validando...' : 'Aplicar' }}
              </button>
            </div>
            <div v-else class="flex items-center justify-between bg-green-50 border-2 border-green-400 p-3">
              <div>
                <p class="font-black text-sm uppercase text-green-700">
                  {{ appliedCoupon.code }}
                  <span v-if="appliedCoupon.discount_type === 'PERCENTAGE'">
                    - {{ appliedCoupon.discount_value }}%
                  </span>
                  <span v-else>
                    - ${{ formatPrice(appliedCoupon.discount_value) }}
                  </span>
                </p>
                <p class="text-xs text-green-600">Cupon aplicado correctamente</p>
              </div>
              <button class="p-1 hover:bg-green-100" @click="removeCoupon">
                <XCircle :size="20" :stroke-width="2.5" class="text-green-700" />
              </button>
            </div>
            <p v-if="couponError" class="text-xs text-red-600 font-bold mt-2">{{ couponError }}</p>
          </div>

          <!-- Totals -->
          <div class="brutal-card p-5">
            <div class="space-y-2 mb-4">
              <div class="flex justify-between text-sm font-bold">
                <span>Subtotal</span>
                <span>${{ formatPrice(cartTotal) }}</span>
              </div>
              <div class="flex justify-between text-sm font-bold">
                <span>Envio</span>
                <span>${{ formatPrice(String(shippingCost)) }}</span>
              </div>
              <div v-if="appliedCoupon" class="flex justify-between text-sm font-bold text-green-700">
                <span>Descuento ({{ appliedCoupon.code }})</span>
                <span>-${{ formatPrice(String(couponDiscount)) }}</span>
              </div>
              <div class="border-t-4 border-brutal-black pt-2 flex justify-between items-center">
                <span class="font-black text-xl uppercase">Total</span>
                <span class="font-black text-2xl">${{ formatPrice(String(grandTotal)) }}</span>
              </div>
            </div>
            <p class="text-xs text-brutal-black/50 mb-4">
              Al confirmar se creara tu pedido y se descontara el inventario.
              Estado inicial: <strong>{{ orderStatusLabels.PENDING }}</strong>.
            </p>

            <div class="flex flex-col sm:flex-row gap-3">
              <button
                class="brutal-button bg-brutal-white text-brutal-black px-6 py-3 flex items-center justify-center gap-2 uppercase tracking-wide"
                @click="goBack"
              >
                <ArrowLeft :size="18" :stroke-width="2.5" />
                Volver
              </button>
              <button
                class="brutal-button bg-brutal-yellow text-brutal-black px-6 py-4 flex-1 flex items-center justify-center gap-2 uppercase tracking-wide disabled:opacity-60"
                :disabled="processing"
                @click="placeOrder"
              >
                <ShoppingBag :size="18" :stroke-width="2.5" />
                {{ processing ? 'Procesando...' : 'Confirmar pedido' }}
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <Teleport to="body">
    <div
      v-if="showSandboxConfirm"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div class="absolute inset-0 bg-brutal-black/50" @click="showSandboxConfirm = false"></div>
      <div class="relative bg-brutal-white brutal-border brutal-shadow p-8 w-full max-w-md text-center space-y-4">
        <div class="bg-brutal-yellow p-3 brutal-border inline-block mx-auto">
          <CheckCircle2 :size="32" :stroke-width="2.5" />
        </div>
        <h3 class="font-black text-xl uppercase">Confirmar pago (sandbox)</h3>
        <p class="text-brutal-black/70 text-sm">
          No hay credenciales de MercadoPago configuradas. En modo sandbox, confirma el pago manualmente para simular la aprobacion.
        </p>
        <div class="flex flex-col gap-2 pt-2">
          <button
            class="brutal-button bg-green-500 text-brutal-white px-6 py-3 uppercase tracking-wide flex items-center justify-center gap-2 disabled:opacity-60"
            :disabled="paying"
            @click="confirmSandboxPayment"
          >
            <CheckCircle2 :size="18" :stroke-width="2.5" />
            {{ paying ? 'Procesando...' : 'Confirmar pago aprobado' }}
          </button>
          <button
            class="brutal-button bg-brutal-white text-brutal-black px-6 py-2 text-sm uppercase tracking-wide"
            @click="showSandboxConfirm = false"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
