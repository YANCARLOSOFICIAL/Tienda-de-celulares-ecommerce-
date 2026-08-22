<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Star, MessageSquare, Trash2 } from '@lucide/vue'

import { reviewsApi, type Review, type RatingSummary, type ReviewPayload } from '../api/reviews'
import { useAuthStore } from '../stores/auth'

const props = defineProps<{ productId: number }>()

const authStore = useAuthStore()

const reviews = ref<Review[]>([])
const summary = ref<RatingSummary>({ average: 0, total: 0, distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 } })
const loading = ref(true)
const showForm = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)

const form = ref<ReviewPayload>({ product_id: props.productId, rating: 5, title: '', comment: '' })
const hoverRating = ref(0)

const myReview = computed(() =>
  reviews.value.find((r) => r.user_id === authStore.user?.id) ?? null,
)

onMounted(fetchData)

async function fetchData() {
  loading.value = true
  try {
    const [r, s] = await Promise.all([
      reviewsApi.listForProduct(props.productId),
      reviewsApi.getRatingSummary(props.productId),
    ])
    reviews.value = r
    summary.value = s
  } catch {
    reviews.value = []
  } finally {
    loading.value = false
  }
}

function openForm() {
  if (myReview.value) {
    form.value = { product_id: props.productId, rating: myReview.value.rating, title: myReview.value.title ?? '', comment: myReview.value.comment ?? '' }
  } else {
    form.value = { product_id: props.productId, rating: 5, title: '', comment: '' }
  }
  error.value = null
  showForm.value = true
}

async function submitReview() {
  saving.value = true
  error.value = null
  try {
    if (myReview.value) {
      await reviewsApi.update(myReview.value.id, form.value)
    } else {
      await reviewsApi.create(form.value)
    }
    showForm.value = false
    await fetchData()
  } catch (e: any) {
    error.value = e.message || 'Error al guardar la review'
  } finally {
    saving.value = false
  }
}

async function deleteReview(id: number) {
  if (!confirm('Eliminar tu review?')) return
  await reviewsApi.remove(id)
  await fetchData()
}

function ratingLabel(stars: number): string {
  const labels = ['', 'Muy mala', 'Mala', 'Regular', 'Buena', 'Excelente']
  return labels[stars] || ''
}

function barWidth(stars: number): number {
  if (summary.value.total === 0) return 0
  return (summary.value.distribution[stars] / summary.value.total) * 100
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h3 class="font-black text-xl uppercase flex items-center gap-2">
        <MessageSquare :size="20" :stroke-width="2.5" />
        Reviews
        <span class="text-sm font-bold text-text/50">({{ summary.total }})</span>
      </h3>
      <button
        v-if="authStore.isAuthenticated && !myReview"
        class="btn-primary text-text px-4 py-2 text-sm uppercase tracking-wide"
        @click="openForm"
      >
        Escribir review
      </button>
      <button
        v-else-if="authStore.isAuthenticated && myReview"
        class="btn-secondary text-text px-4 py-2 text-sm uppercase tracking-wide"
        @click="openForm"
      >
        Editar mi review
      </button>
    </div>

    <!-- Rating Summary -->
    <div v-if="summary.total > 0" class="bento-card p-5 flex flex-col sm:flex-row gap-6">
      <div class="text-center sm:text-left shrink-0">
        <p class="font-black text-5xl">{{ summary.average }}</p>
        <div class="flex items-center gap-0.5 mt-1 justify-center sm:justify-start">
          <Star v-for="i in 5" :key="i" :size="16" :stroke-width="2.5"
            :class="i <= Math.round(summary.average) ? 'text-amber-400 fill-amber-400' : 'text-text/20'"
          />
        </div>
        <p class="text-xs text-text/50 mt-1">{{ summary.total }} review{{ summary.total !== 1 ? 's' : '' }}</p>
      </div>
      <div class="flex-1 space-y-1.5">
        <div v-for="stars in [5, 4, 3, 2, 1]" :key="stars" class="flex items-center gap-2 text-sm">
          <span class="w-8 text-right font-bold">{{ stars }}</span>
          <Star :size="12" :stroke-width="2.5" class="text-amber-400 fill-amber-400 shrink-0" />
          <div class="flex-1 h-2.5 bg-border-light rounded-full overflow-hidden">
            <div class="h-full bg-amber-400 rounded-full transition-all" :style="{ width: barWidth(stars) + '%' }"></div>
          </div>
          <span class="w-6 text-xs font-bold text-text/50">{{ summary.distribution[stars] }}</span>
        </div>
      </div>
    </div>

    <!-- Review Form -->
    <div v-if="showForm" class="bento-card p-5 space-y-4">
      <h4 class="font-black text-lg uppercase">{{ myReview ? 'Editar review' : 'Tu review' }}</h4>
      <div v-if="error" class="bg-red-100 border-2 border-red-400 p-3 text-sm font-bold text-red-700">{{ error }}</div>

      <div>
        <label class="font-bold text-xs uppercase tracking-wide block mb-2">Calificacion</label>
        <div class="flex items-center gap-1">
          <button
            v-for="i in 5"
            :key="i"
            class="p-0.5 transition-transform hover:scale-110"
            @mouseenter="hoverRating = i"
            @mouseleave="hoverRating = 0"
            @click="form.rating = i"
          >
            <Star
              :size="28" :stroke-width="2.5"
              :class="(hoverRating || form.rating) >= i ? 'text-amber-400 fill-amber-400' : 'text-text/20'"
            />
          </button>
          <span v-if="hoverRating || form.rating" class="text-sm font-bold ml-2">
            {{ ratingLabel(hoverRating || form.rating) }}
          </span>
        </div>
      </div>

      <div>
        <label class="font-bold text-xs uppercase tracking-wide block mb-1">Titulo (opcional)</label>
        <input
          v-model="form.title"
          class="w-full input-minimal"
          placeholder="Resumen de tu experiencia"
          maxlength="200"
        />
      </div>

      <div>
        <label class="font-bold text-xs uppercase tracking-wide block mb-1">Comentario (opcional)</label>
        <textarea
          v-model="form.comment"
          rows="3"
          class="w-full input-minimal resize-none"
          placeholder="Cuenta tu experiencia con el producto..."
          maxlength="2000"
        />
      </div>

      <div class="flex justify-end gap-2">
        <button
          class="btn-secondary text-text px-4 py-2 text-sm uppercase tracking-wide"
          @click="showForm = false"
        >
          Cancelar
        </button>
        <button
          class="btn-primary text-text px-4 py-2 text-sm uppercase tracking-wide disabled:opacity-60"
          :disabled="saving || !form.rating"
          @click="submitReview"
        >
          {{ saving ? 'Guardando...' : myReview ? 'Actualizar' : 'Publicar' }}
        </button>
      </div>
    </div>

    <!-- Reviews List -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="bento-card p-4 space-y-2">
        <div class="skeleton h-4 w-32"></div>
        <div class="skeleton h-3 w-full"></div>
      </div>
    </div>

    <div v-else-if="reviews.length === 0 && !showForm" class="bento-card p-8 text-center">
      <MessageSquare :size="36" :stroke-width="1.5" class="mx-auto text-text/20 mb-3" />
      <p class="font-black text-lg uppercase">Sin reviews</p>
      <p class="text-text/50 text-sm mt-1">Sé el primero en dejar tu opinion.</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="bento-card p-4"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <div class="flex items-center gap-0.5">
                <Star v-for="i in 5" :key="i" :size="14" :stroke-width="2.5"
                  :class="i <= review.rating ? 'text-amber-400 fill-amber-400' : 'text-text/20'"
                />
              </div>
              <span class="text-xs font-bold text-text/50">{{ review.user_name }}</span>
            </div>
            <p v-if="review.title" class="font-black text-sm">{{ review.title }}</p>
            <p v-if="review.comment" class="text-sm text-text/70 mt-1">{{ review.comment }}</p>
          </div>
          <button
            v-if="authStore.user?.id === review.user_id"
            class="p-1.5 hover:bg-red-100 text-red-600 shrink-0"
            title="Eliminar"
            @click="deleteReview(review.id)"
          >
            <Trash2 :size="14" :stroke-width="2.5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
