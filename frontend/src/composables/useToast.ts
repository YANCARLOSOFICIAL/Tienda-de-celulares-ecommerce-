import { reactive } from 'vue'

export type ToastKind = 'success' | 'error' | 'info'

export interface Toast {
  id: number
  kind: ToastKind
  message: string
}

const toasts = reactive<Toast[]>([])
let nextId = 1

const DEFAULT_DURATION = 4000

function dismiss(id: number) {
  const idx = toasts.findIndex((t) => t.id === id)
  if (idx !== -1) toasts.splice(idx, 1)
}

function push(kind: ToastKind, message: string, duration = DEFAULT_DURATION) {
  const id = nextId++
  toasts.push({ id, kind, message })
  if (duration > 0) {
    window.setTimeout(() => dismiss(id), duration)
  }
  return id
}

/**
 * Notificaciones ligeras (toasts). Estado global compartido: se renderiza una
 * sola vez con <Toaster /> en App.vue.
 *
 *   const toast = useToast()
 *   toast.success('Producto agregado al carrito')
 *   toast.error(err instanceof ApiError ? err.message : 'Algo salió mal')
 */
export function useToast() {
  return {
    toasts,
    dismiss,
    success: (msg: string, duration?: number) => push('success', msg, duration),
    error: (msg: string, duration?: number) => push('error', msg, duration),
    info: (msg: string, duration?: number) => push('info', msg, duration),
  }
}
