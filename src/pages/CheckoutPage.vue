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
    await paymentsApi.confirm(createdPaymentId.value)
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
  <section class="min-h-screen bg-surface">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 py-12 sm:py-16">

      <!-- SUCCESS SCREEN -->
      <div v-if="createdOrderId" class="text-center py-16">
        <div class="w-16 h-16 rounded-full bg-neon-green/10 flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 :size="32" :stroke-width="1.5" class="text-neon-green" />
        </div>
        <h2 class="text-3xl font-semibold text-text tracking-tight mb-2">Pedido confirmado</h2>
        <p class="text-text-secondary mb-8">
          Tu pedido #{{ createdOrderId }} fue registrado con exito.
        </p>
        <div class="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            class="btn-primary px-8 py-3 flex items-center justify-center gap-2"
            :disabled="paying"
            @click="payNow"
          >
            {{ paying ? 'Redirigiendo...' : 'Pagar ahora' }}
          </button>
          <router-link
            to="/orders"
            class="btn-secondary px-8 py-3 text-center"
          >
            Ver mis pedidos
          </router-link>
          <router-link
            to="/#productos"
            class="btn-secondary px-8 py-3 text-center"
          >
            Seguir comprando
          </router-link>
        </div>
      </div>

      <!-- LOADING -->
      <div v-else-if="cartStore.loading" class="text-center py-20">
        <div class="w-48 h-4 mx-auto mb-4 rounded skeleton"></div>
        <div class="w-32 h-4 mx-auto rounded skeleton"></div>
      </div>

      <!-- EMPTY CART -->
      <div v-else-if="isEmpty" class="text-center py-16">
        <ShoppingBag :size="48" :stroke-width="1" class="text-text-secondary mx-auto mb-4" />
        <h2 class="text-2xl font-semibold text-text tracking-tight mb-2">Carrito vacio</h2>
        <p class="text-text-secondary mb-6">No hay productos en tu carrito.</p>
        <router-link
          to="/#productos"
          class="btn-primary px-8 py-3 inline-block"
        >
          Ver catalogo
        </router-link>
      </div>

      <!-- CHECKOUT FLOW -->
      <div v-else>
        <div class="mb-10">
          <h1 class="text-3xl font-semibold text-text tracking-tight">Checkout</h1>
        </div>

        <!-- Progress Steps -->
        <div class="flex items-center mb-10">
          <template v-for="(label, i) in stepLabels" :key="i">
            <div class="flex items-center gap-2">
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium transition-all"
                :class="step === i + 1
                  ? 'bg-accent text-black neon-border'
                  : step > i + 1
                    ? 'bg-neon-green text-black'
                    : 'bg-surface-dim text-text-secondary border border-border'"
              >
                <CheckCircle2 v-if="step > i + 1" :size="14" :stroke-width="2.5" />
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span
                class="text-xs font-medium hidden sm:block"
                :class="step === i + 1 ? 'text-text neon-text' : 'text-text-secondary'"
              >
                {{ label }}
              </span>
            </div>
            <div
              v-if="i < stepLabels.length - 1"
              class="flex-1 h-px mx-3"
              :class="step > i + 1 ? 'bg-neon-green' : 'bg-border'"
            ></div>
          </template>
        </div>

        <!-- Error -->
        <div
          v-if="orderError"
          class="mb-6 p-4 rounded-xl bg-danger/5 border border-danger/20 flex items-center gap-3"
        >
          <XCircle :size="18" :stroke-width="2" class="text-danger flex-shrink-0" />
          <p class="text-sm text-danger">{{ orderError }}</p>
        </div>

        <!-- STEP 1: ADDRESS -->
        <div v-if="step === 1" class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-text mb-4 flex items-center gap-2">
              <MapPin :size="18" :stroke-width="1.5" class="text-text-secondary" />
              Direccion de entrega
            </h2>

            <div v-if="addresses.length === 0 && !showNewAddress" class="text-text-secondary text-sm">
              No tienes direcciones guardadas.
            </div>

            <div v-else class="space-y-3 mb-4">
              <button
                v-for="addr in addresses"
                :key="addr.id"
                class="w-full text-left rounded-xl p-4 transition-all"
                :class="selectedAddressId === addr.id
                  ? 'neon-border bg-accent/[0.03]'
                  : 'border border-border hover:border-accent/40 bg-surface-dim'"
                @click="selectAddress(addr.id)"
              >
                <div class="flex items-start justify-between">
                  <div class="min-w-0">
                    <p class="text-sm font-medium text-text">
                      {{ addr.label || 'Direccion' }}
                      <span v-if="addr.is_default" class="badge-accent text-[10px] ml-2">
                        Default
                      </span>
                    </p>
                    <p class="text-sm text-text-secondary mt-1">
                      {{ addr.street }} {{ addr.street_number }}
                      <span v-if="addr.interior">, {{ addr.interior }}</span>
                    </p>
                    <p class="text-sm text-text-secondary">
                      {{ addr.neighborhood }}, {{ addr.city }}, {{ addr.state }} {{ addr.zip_code }}
                    </p>
                    <p class="text-xs text-text-tertiary mt-1">
                      {{ addr.full_name }} - {{ addr.phone }}
                    </p>
                  </div>
                  <div
                    v-if="selectedAddressId === addr.id"
                    class="w-5 h-5 rounded-full bg-accent flex items-center justify-center flex-shrink-0 mt-0.5"
                  >
                    <CheckCircle2 :size="12" class="text-black" :stroke-width="2.5" />
                  </div>
                  <div
                    v-else
                    class="w-5 h-5 rounded-full border-2 border-border flex-shrink-0 mt-0.5"
                  ></div>
                </div>
              </button>
            </div>

            <button
              class="text-sm text-accent font-medium flex items-center gap-1.5 hover:opacity-70 transition-opacity"
              @click="toggleNewAddress"
            >
              <Plus :size="16" :stroke-width="2" />
              {{ showNewAddress ? 'Cancelar' : 'Agregar direccion nueva' }}
            </button>
          </div>

          <!-- NEW ADDRESS FORM -->
          <div v-if="showNewAddress" class="glass-dark rounded-2xl p-6 space-y-4">
            <h3 class="text-base font-semibold text-text">Nueva direccion</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Etiqueta</label>
                <input
                  v-model="newAddress.label"
                  placeholder="Casa, Oficina..."
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Nombre completo *</label>
                <input
                  v-model="newAddress.full_name"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Telefono *</label>
                <input
                  v-model="newAddress.phone"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Calle *</label>
                <input
                  v-model="newAddress.street"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Numero</label>
                <input
                  v-model="newAddress.street_number"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Interior</label>
                <input
                  v-model="newAddress.interior"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Colonia *</label>
                <input
                  v-model="newAddress.neighborhood"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Ciudad *</label>
                <input
                  v-model="newAddress.city"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Estado *</label>
                <input
                  v-model="newAddress.state"
                  class="input-minimal"
                />
              </div>
              <div>
                <label class="text-xs font-medium text-text-secondary block mb-1.5">Codigo postal *</label>
                <input
                  v-model="newAddress.zip_code"
                  class="input-minimal"
                />
              </div>
            </div>
            <button
              class="btn-primary px-5 py-2.5"
              @click="saveNewAddress"
            >
              Guardar direccion
            </button>
          </div>

          <div class="flex justify-end pt-2">
            <button
              class="btn-primary px-8 py-3 flex items-center gap-2"
              :disabled="!selectedAddressId && !showNewAddress"
              @click="goNext"
            >
              Continuar
              <ChevronRight :size="16" :stroke-width="2" />
            </button>
          </div>
        </div>

        <!-- STEP 2: SHIPPING METHOD -->
        <div v-if="step === 2" class="space-y-6">
          <div>
            <h2 class="text-lg font-semibold text-text mb-4 flex items-center gap-2">
              <Truck :size="18" :stroke-width="1.5" class="text-text-secondary" />
              Metodo de envio
            </h2>

            <div class="space-y-3">
              <label
                v-for="method in ['ESTANDAR', 'EXPRESS', 'RECOLECCION']"
                :key="method"
                class="flex items-center gap-4 rounded-xl p-4 cursor-pointer transition-all"
                :class="shippingMethod === method
                  ? 'neon-border bg-accent/[0.03]'
                  : 'border border-border hover:border-accent/40 bg-surface-dim'"
              >
                <input
                  v-model="shippingMethod"
                  type="radio"
                  :value="method"
                  class="w-4 h-4 accent-accent"
                />
                <div class="flex-1">
                  <span class="text-sm font-medium text-text">
                    {{ method === 'ESTANDAR' ? 'Estandar' : method === 'EXPRESS' ? 'Express' : 'Recoleccion en tienda' }}
                  </span>
                  <span class="text-xs text-text-secondary ml-2">
                    {{ method === 'ESTANDAR' ? '5-7 dias habiles' : method === 'EXPRESS' ? '1-2 dias habiles' : 'Sin costo' }}
                  </span>
                </div>
                <span class="text-sm font-medium text-text">
                  {{ method === 'ESTANDAR' ? '$99' : method === 'EXPRESS' ? '$199' : '$0' }}
                </span>
              </label>
            </div>
          </div>

          <div class="flex justify-between pt-2">
            <button
              class="btn-secondary px-6 py-3 flex items-center gap-2"
              @click="goBack"
            >
              <ArrowLeft :size="16" :stroke-width="2" />
              Volver
            </button>
            <button
              class="btn-primary px-8 py-3 flex items-center gap-2"
              @click="goNext"
            >
              Continuar
              <ChevronRight :size="16" :stroke-width="2" />
            </button>
          </div>
        </div>

        <!-- STEP 3: ORDER SUMMARY -->
        <div v-if="step === 3" class="space-y-6">
          <!-- Products -->
          <div>
            <h2 class="text-lg font-semibold text-text mb-4 flex items-center gap-2">
              <FileText :size="18" :stroke-width="1.5" class="text-text-secondary" />
              Resumen del pedido
            </h2>
            <div class="space-y-3">
              <div
                v-for="item in items"
                :key="item.id"
                class="flex items-center gap-4 py-3 border-b border-border last:border-b-0"
              >
                <div class="w-14 h-14 rounded-xl bg-surface-dim flex items-center justify-center flex-shrink-0 overflow-hidden">
                  <img
                    v-if="item.product.image"
                    :src="item.product.image"
                    :alt="item.product.name"
                    class="w-full h-full object-cover"
                  />
                  <ShoppingBag v-else :size="20" :stroke-width="1.5" class="text-text-secondary" />
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-sm font-medium text-text truncate">{{ item.product.name }}</p>
                  <p class="text-xs text-text-secondary mt-0.5">
                    ${{ formatPrice(item.product.price) }} x {{ item.quantity }}
                  </p>
                </div>
                <span class="text-sm font-medium text-text whitespace-nowrap">${{ formatPrice(item.subtotal) }}</span>
              </div>
            </div>
          </div>

          <!-- Address & Shipping -->
          <div class="glass-dark rounded-2xl p-5 space-y-3">
            <div v-if="selectedAddress" class="flex items-start gap-3">
              <MapPin :size="18" :stroke-width="1.5" class="text-text-secondary mt-0.5 flex-shrink-0" />
              <div>
                <p class="text-sm font-medium text-text">{{ selectedAddress.label || 'Direccion' }}</p>
                <p class="text-sm text-text-secondary mt-0.5">
                  {{ selectedAddress.street }} {{ selectedAddress.street_number }}
                  <span v-if="selectedAddress.interior">, {{ selectedAddress.interior }}</span>
                </p>
                <p class="text-sm text-text-secondary">
                  {{ selectedAddress.neighborhood }}, {{ selectedAddress.city }}, {{ selectedAddress.state }} {{ selectedAddress.zip_code }}
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <Truck :size="18" :stroke-width="1.5" class="text-text-secondary" />
              <span class="text-sm text-text">{{ shipLabel(shippingMethod) }}</span>
            </div>
          </div>

          <!-- Notes -->
          <div>
            <label class="text-sm font-medium text-text block mb-2">
              Notas adicionales
              <span class="text-text-secondary font-normal">(opcional)</span>
            </label>
            <textarea
              v-model="notes"
              rows="3"
              placeholder="Instrucciones de entrega, referencias..."
              class="input-minimal resize-none"
            />
          </div>

          <!-- Coupon -->
          <div>
            <label class="text-sm font-medium text-text block mb-2">Cupon de descuento</label>
            <div v-if="!appliedCoupon" class="flex gap-2">
              <input
                v-model="couponCode"
                class="input-minimal flex-1 uppercase"
                placeholder="Codigo del cupon"
                @keyup.enter="applyCoupon"
              />
              <button
                class="btn-secondary px-5 py-2.5 disabled:opacity-50"
                :disabled="validatingCoupon || !couponCode.trim()"
                @click="applyCoupon"
              >
                {{ validatingCoupon ? 'Validando...' : 'Aplicar' }}
              </button>
            </div>
            <div v-else class="flex items-center justify-between bg-neon-green/5 border border-neon-green/20 rounded-xl p-3">
              <div>
                <p class="text-sm font-medium text-neon-green">
                  {{ appliedCoupon.code }}
                  <span v-if="appliedCoupon.discount_type === 'PERCENTAGE'">
                    - {{ appliedCoupon.discount_value }}%
                  </span>
                  <span v-else>
                    - ${{ formatPrice(appliedCoupon.discount_value) }}
                  </span>
                </p>
                <p class="text-xs text-neon-green/70 mt-0.5">Cupon aplicado correctamente</p>
              </div>
              <button class="p-1.5 rounded-full hover:bg-neon-green/10 transition-colors" @click="removeCoupon">
                <XCircle :size="18" :stroke-width="2" class="text-neon-green" />
              </button>
            </div>
            <p v-if="couponError" class="text-xs text-danger mt-2">{{ couponError }}</p>
          </div>

          <!-- Totals -->
          <div class="glass-dark rounded-2xl p-5">
            <div class="space-y-2.5 mb-4">
              <div class="flex justify-between text-sm text-text">
                <span>Subtotal</span>
                <span>${{ formatPrice(cartTotal) }}</span>
              </div>
              <div class="flex justify-between text-sm text-text">
                <span>Envio</span>
                <span>${{ formatPrice(String(shippingCost)) }}</span>
              </div>
              <div v-if="appliedCoupon" class="flex justify-between text-sm text-neon-green">
                <span>Descuento ({{ appliedCoupon.code }})</span>
                <span>-${{ formatPrice(String(couponDiscount)) }}</span>
              </div>
              <div class="border-t border-border pt-3 mt-3 flex justify-between items-center">
                <span class="text-lg font-semibold text-text">Total</span>
                <span class="text-2xl font-bold text-text">${{ formatPrice(String(grandTotal)) }}</span>
              </div>
            </div>
            <p class="text-xs text-text-secondary mb-5">
              Al confirmar se creara tu pedido y se descontara el inventario.
              Estado inicial: <strong class="text-text">{{ orderStatusLabels.PENDING }}</strong>.
            </p>

            <div class="flex flex-col sm:flex-row gap-3">
              <button
                class="btn-secondary px-6 py-3 flex items-center justify-center gap-2"
                @click="goBack"
              >
                <ArrowLeft :size="16" :stroke-width="2" />
                Volver
              </button>
              <button
                class="btn-primary px-8 py-4 flex-1 flex items-center justify-center gap-2"
                :disabled="processing"
                @click="placeOrder"
              >
                <ShoppingBag :size="16" :stroke-width="2" />
                {{ processing ? 'Procesando...' : 'Confirmar pedido' }}
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- SANDBOX PAYMENT MODAL -->
  <Teleport to="body">
    <div
      v-if="showSandboxConfirm"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
    >
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="showSandboxConfirm = false"></div>
      <div class="relative glass-dark rounded-2xl p-8 w-full max-w-md text-center space-y-5 shadow-lg">
        <div class="w-14 h-14 rounded-full bg-accent/10 flex items-center justify-center mx-auto">
          <CheckCircle2 :size="28" :stroke-width="1.5" class="text-accent" />
        </div>
        <h3 class="text-xl font-semibold text-text">Confirmar pago (sandbox)</h3>
        <p class="text-text-secondary text-sm leading-relaxed">
          No hay credenciales de MercadoPago configuradas. En modo sandbox, confirma el pago manualmente para simular la aprobacion.
        </p>
        <div class="flex flex-col gap-2.5 pt-1">
          <button
            class="bg-neon-green text-black px-6 py-3 rounded-full text-sm font-medium flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-50"
            :disabled="paying"
            @click="confirmSandboxPayment"
          >
            <CheckCircle2 :size="16" :stroke-width="2" />
            {{ paying ? 'Procesando...' : 'Confirmar pago aprobado' }}
          </button>
          <button
            class="btn-secondary px-6 py-2.5"
            @click="showSandboxConfirm = false"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
