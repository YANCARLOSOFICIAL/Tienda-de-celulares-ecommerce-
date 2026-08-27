<script setup lang="ts">
import { CheckCircle2, AlertCircle, Info, X } from '@lucide/vue'
import { useToast, type ToastKind } from '@/composables/useToast'

const { toasts, dismiss } = useToast()

const icon: Record<ToastKind, typeof CheckCircle2> = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
}

const accent: Record<ToastKind, string> = {
  success: 'text-success',
  error: 'text-danger',
  info: 'text-accent',
}
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[60] flex flex-col items-center gap-2 w-[calc(100%-2rem)] max-w-sm"
      role="region"
      aria-label="Notificaciones"
    >
      <TransitionGroup
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 translate-y-3"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in absolute"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div
          v-for="t in toasts"
          :key="t.id"
          class="glass-strong w-full rounded-xl shadow-2xl shadow-black/40 px-4 py-3 flex items-start gap-3"
          role="status"
          aria-live="polite"
        >
          <component :is="icon[t.kind]" :size="18" :stroke-width="2" class="shrink-0 mt-0.5" :class="accent[t.kind]" />
          <p class="text-sm text-text flex-1 leading-snug">{{ t.message }}</p>
          <button
            class="shrink-0 text-text-tertiary hover:text-text transition-colors"
            aria-label="Cerrar notificación"
            @click="dismiss(t.id)"
          >
            <X :size="15" :stroke-width="2" />
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
