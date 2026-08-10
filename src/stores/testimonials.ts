import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Testimonial {
  id: number
  name: string
  text: string
  rating: number
  avatar: string
}

export const useTestimonialsStore = defineStore('testimonials', () => {
  const testimonials = ref<Testimonial[]>([
    {
      id: 1,
      name: 'María García',
      text: 'Excelente atención. Me asesoraron para elegir el mejor celular y el envío fue súper rápido. ¡Totalmente recomendados!',
      rating: 5,
      avatar: 'https://placehold.co/80x80/FFD60A/111111?text=MG&font=inter'
    },
    {
      id: 2,
      name: 'Carlos López',
      text: 'Compré un Samsung Galaxy y llegó en perfecto estado. El precio fue el mejor que encontré en todo el mercado.',
      rating: 5,
      avatar: 'https://placehold.co/80x80/FFD60A/111111?text=CL&font=inter'
    },
    {
      id: 3,
      name: 'Ana Martínez',
      text: 'Repararon mi iPhone en tiempo récord. Muy profesionales y con garantía incluida. Volveré sin duda.',
      rating: 5,
      avatar: 'https://placehold.co/80x80/FFD60A/111111?text=AM&font=inter'
    },
    {
      id: 4,
      name: 'Roberto Sánchez',
      text: 'Compré un Xiaomi 14 con descuento por lanzamiento. Me ayudaron a transferir todos mis datos. Servicio increíble.',
      rating: 5,
      avatar: 'https://placehold.co/80x80/FFD60A/111111?text=RS&font=inter'
    }
  ])

  return { testimonials }
})
