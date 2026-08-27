import { ref, onMounted, onUnmounted, type Ref } from 'vue'

export function useIntersectionObserver(
  elementRef: Ref<HTMLElement | null>,
  options: IntersectionObserverInit = { threshold: 0.15 }
) {
  const isVisible = ref(false)
  let observer: IntersectionObserver | null = null

  onMounted(() => {
    if (!elementRef.value) return

    observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer?.unobserve(entry.target)
      }
    }, options)

    observer.observe(elementRef.value)
  })

  onUnmounted(() => {
    observer?.disconnect()
  })

  return { isVisible }
}
