<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '../composables/useIntersectionObserver'
import { Send, CheckCircle, AlertCircle, Phone, Mail, MapPin } from '@lucide/vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionObserver(sectionRef)

const form = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const status = ref<'idle' | 'sending' | 'success' | 'error'>('idle')
const errors = ref<Record<string, string>>({})

function validate(): boolean {
  errors.value = {}
  if (!form.value.name.trim()) errors.value.name = 'El nombre es obligatorio'
  if (!form.value.email.trim()) errors.value.email = 'El correo es obligatorio'
  else if (!/\S+@\S+\.\S+/.test(form.value.email)) errors.value.email = 'Correo inválido'
  if (!form.value.message.trim()) errors.value.message = 'El mensaje es obligatorio'
  return Object.keys(errors.value).length === 0
}

async function handleSubmit() {
  if (!validate()) return
  status.value = 'sending'

  try {
    await new Promise(resolve => setTimeout(resolve, 1500))
    status.value = 'success'
    form.value = { name: '', email: '', phone: '', message: '' }
    setTimeout(() => { status.value = 'idle' }, 4000)
  } catch {
    status.value = 'error'
  }
}

const contactInfo = [
  { icon: Phone, label: 'Teléfono', value: '+52 123 456 7890' },
  { icon: Mail, label: 'Email', value: 'hola@tiendacell.mx' },
  { icon: MapPin, label: 'Dirección', value: 'Av. Tecnológico 123, Col. Centro, CDMX' }
]
</script>

<template>
  <section
    id="contacto"
    ref="sectionRef"
    class="py-16 sm:py-20 lg:py-28 bg-brutal-gray"
    aria-labelledby="contacto-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="inline-block bg-brutal-yellow text-brutal-black font-bold text-sm px-4 py-2 brutal-border mb-4">
          CONTACTO
        </span>
        <h2 id="contacto-title" class="section-title text-brutal-black mb-4">
          Escríbenos
        </h2>
        <p class="section-subtitle">
          Estamos listos para ayudarte. Contáctanos por cualquier duda o consulta.
        </p>
      </div>

      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-start">
        <div
          :class="[
            'brutal-card !bg-brutal-white p-6 sm:p-8',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
        >
          <form @submit.prevent="handleSubmit" novalidate class="space-y-5">
            <div>
              <label for="name" class="block font-bold text-sm mb-1 uppercase tracking-wide">Nombre *</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="w-full brutal-border px-4 py-3 bg-brutal-white font-medium text-base focus:outline-none focus:ring-0 focus:bg-brutal-yellow/10"
                :class="{ 'border-red-500': errors.name }"
                placeholder="Tu nombre"
              />
              <p v-if="errors.name" class="text-red-600 font-bold text-sm mt-1 flex items-center gap-1">
                <AlertCircle :size="14" /> {{ errors.name }}
              </p>
            </div>

            <div>
              <label for="email" class="block font-bold text-sm mb-1 uppercase tracking-wide">Correo electrónico *</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="w-full brutal-border px-4 py-3 bg-brutal-white font-medium text-base focus:outline-none focus:ring-0 focus:bg-brutal-yellow/10"
                :class="{ 'border-red-500': errors.email }"
                placeholder="tu@correo.com"
              />
              <p v-if="errors.email" class="text-red-600 font-bold text-sm mt-1 flex items-center gap-1">
                <AlertCircle :size="14" /> {{ errors.email }}
              </p>
            </div>

            <div>
              <label for="phone" class="block font-bold text-sm mb-1 uppercase tracking-wide">Teléfono</label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                class="w-full brutal-border px-4 py-3 bg-brutal-white font-medium text-base focus:outline-none focus:ring-0 focus:bg-brutal-yellow/10"
                placeholder="+52 55 1234 5678"
              />
            </div>

            <div>
              <label for="message" class="block font-bold text-sm mb-1 uppercase tracking-wide">Mensaje *</label>
              <textarea
                id="message"
                v-model="form.message"
                rows="4"
                class="w-full brutal-border px-4 py-3 bg-brutal-white font-medium text-base resize-y focus:outline-none focus:ring-0 focus:bg-brutal-yellow/10"
                :class="{ 'border-red-500': errors.message }"
                placeholder="¿En qué podemos ayudarte?"
              ></textarea>
              <p v-if="errors.message" class="text-red-600 font-bold text-sm mt-1 flex items-center gap-1">
                <AlertCircle :size="14" /> {{ errors.message }}
              </p>
            </div>

            <button
              type="submit"
              class="brutal-button bg-brutal-black text-brutal-white px-8 py-3 text-base uppercase tracking-wide flex items-center justify-center gap-2 w-full disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="status === 'sending'"
            >
              <template v-if="status === 'sending'">
                <span class="inline-block w-5 h-5 border-2 border-brutal-white border-t-transparent rounded-full animate-spin"></span>
                Enviando...
              </template>
              <template v-else-if="status === 'success'">
                <CheckCircle :size="20" class="text-whatsapp" /> Mensaje enviado
              </template>
              <template v-else>
                <Send :size="18" :stroke-width="2.5" /> Enviar mensaje
              </template>
            </button>

            <p v-if="status === 'error'" class="text-red-600 font-bold text-sm text-center mt-2">
              Ocurrió un error. Intenta de nuevo.
            </p>
          </form>
        </div>

        <div
          :class="[
            'space-y-6',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: '200ms' }"
        >
          <div
            v-for="(info, i) in contactInfo"
            :key="info.label"
            :class="[
              'brutal-card !bg-brutal-white p-6 flex items-center gap-4',
              'animate-fade-in-up',
              isVisible ? 'visible' : ''
            ]"
            :style="{ transitionDelay: `${300 + i * 100}ms` }"
          >
            <div class="brutal-border bg-brutal-yellow p-3 flex-shrink-0">
              <component :is="info.icon" :size="22" :stroke-width="2.5" />
            </div>
            <div>
              <p class="font-bold text-sm text-brutal-black/60 uppercase tracking-wide">{{ info.label }}</p>
              <p class="font-black text-base sm:text-lg">{{ info.value }}</p>
            </div>
          </div>

          <div
            :class="[
              'animate-fade-in-up',
              isVisible ? 'visible' : ''
            ]"
            :style="{ transitionDelay: '600ms' }"
          >
            <a
              href="https://wa.me/521234567890"
              target="_blank"
              rel="noopener noreferrer"
              class="brutal-button bg-whatsapp text-brutal-white px-8 py-4 text-base uppercase tracking-wide flex items-center justify-center gap-2 w-full"
            >
              <Phone :size="20" :stroke-width="2.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
