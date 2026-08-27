<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionObserver } from '@/composables/useIntersectionObserver'
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
    class="section-clean bg-surface"
    aria-labelledby="contacto-title"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12 sm:mb-16">
        <span class="badge badge-accent mb-4">Contacto</span>
        <h2 id="contacto-title" class="section-title mb-4">
          Escríbenos
        </h2>
        <p class="section-subtitle mx-auto">
          Estamos listos para ayudarte. Contáctanos por cualquier duda o consulta.
        </p>
      </div>

      <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-start">
        <div
          :class="[
            'bento-card p-6 sm:p-8',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
        >
          <form @submit.prevent="handleSubmit" novalidate class="space-y-5">
            <div>
              <label for="name" class="block text-sm font-medium text-text-secondary mb-1.5">Nombre *</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="input-minimal bg-surface-dim border-border text-white placeholder-slate-500 focus:border-blue-500 focus:ring-blue-500/20"
                :class="{ '!border-danger': errors.name }"
                placeholder="Tu nombre"
              />
              <p v-if="errors.name" class="text-danger text-xs mt-1.5 flex items-center gap-1">
                <AlertCircle :size="12" /> {{ errors.name }}
              </p>
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-text-secondary mb-1.5">Correo electrónico *</label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="input-minimal bg-surface-dim border-border text-white placeholder-slate-500 focus:border-blue-500 focus:ring-blue-500/20"
                :class="{ '!border-danger': errors.email }"
                placeholder="tu@correo.com"
              />
              <p v-if="errors.email" class="text-danger text-xs mt-1.5 flex items-center gap-1">
                <AlertCircle :size="12" /> {{ errors.email }}
              </p>
            </div>

            <div>
              <label for="phone" class="block text-sm font-medium text-text-secondary mb-1.5">Teléfono</label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                class="input-minimal bg-surface-dim border-border text-white placeholder-slate-500 focus:border-blue-500 focus:ring-blue-500/20"
                placeholder="+52 55 1234 5678"
              />
            </div>

            <div>
              <label for="message" class="block text-sm font-medium text-text-secondary mb-1.5">Mensaje *</label>
              <textarea
                id="message"
                v-model="form.message"
                rows="4"
                class="input-minimal resize-y bg-surface-dim border-border text-white placeholder-slate-500 focus:border-blue-500 focus:ring-blue-500/20"
                :class="{ '!border-danger': errors.message }"
                placeholder="¿En qué podemos ayudarte?"
              ></textarea>
              <p v-if="errors.message" class="text-danger text-xs mt-1.5 flex items-center gap-1">
                <AlertCircle :size="12" /> {{ errors.message }}
              </p>
            </div>

            <button
              type="submit"
              class="btn-primary w-full flex items-center justify-center gap-2"
              :disabled="status === 'sending'"
            >
              <template v-if="status === 'sending'">
                <span class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Enviando...
              </template>
              <template v-else-if="status === 'success'">
                <CheckCircle :size="18" /> Mensaje enviado
              </template>
              <template v-else>
                <Send :size="16" :stroke-width="2.5" /> Enviar mensaje
              </template>
            </button>

            <p v-if="status === 'error'" class="text-danger text-xs text-center mt-1">
              Ocurrió un error. Intenta de nuevo.
            </p>
          </form>
        </div>

        <div
          :class="[
            'space-y-4',
            'animate-fade-in-up',
            isVisible ? 'visible' : ''
          ]"
          :style="{ transitionDelay: '200ms' }"
        >
          <div
            v-for="(info, i) in contactInfo"
            :key="info.label"
            :class="[
              'bento-card p-5 flex items-center gap-4',
              'animate-fade-in-up',
              isVisible ? 'visible' : ''
            ]"
            :style="{ transitionDelay: `${300 + i * 100}ms` }"
          >
            <div class="w-11 h-11 rounded-xl bg-blue-500/10 flex items-center justify-center flex-shrink-0">
              <component :is="info.icon" :size="18" :stroke-width="2" class="text-blue-500" />
            </div>
            <div>
              <p class="text-xs font-medium text-text-tertiary uppercase tracking-wide">{{ info.label }}</p>
              <p class="font-semibold text-sm text-white">{{ info.value }}</p>
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
              class="flex items-center justify-center gap-2 w-full py-3 px-6 bg-whatsapp text-white font-semibold rounded-full transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <Phone :size="18" :stroke-width="2.5" />
              WhatsApp
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
