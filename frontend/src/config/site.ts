/**
 * Configuración de la tienda. Centraliza país, moneda, datos de contacto,
 * ubicación y reglas de envío para no tener valores "quemados" repartidos
 * por los componentes.
 *
 * Tienda Cell opera en Colombia: los precios se muestran en pesos
 * colombianos (COP, sin decimales) y la facturación electrónica se emite
 * ante la DIAN a través de Factus.
 */

export const site = {
  name: 'Tienda Cell',
  country: 'Colombia',
  countryCode: 'CO',
  locale: 'es-CO',
  currency: 'COP',

  /** Número de WhatsApp en formato internacional sin "+" ni espacios. */
  whatsappNumber: '573001234567',
  /** Teléfono de contacto para mostrar y para enlaces tel:. */
  phoneDisplay: '+57 300 123 4567',
  phoneHref: '+573001234567',
  email: 'hola@tiendacell.com',

  address: {
    line: 'Cra. 7 #71-21, Bogotá D.C.',
    city: 'Bogotá D.C.',
  },

  /**
   * URL de inserción de Google Maps (iframe). Apunta a la sede en Bogotá.
   * Reemplázala por la de la sede real desde Google Maps → Compartir → Insertar un mapa.
   */
  mapEmbedUrl:
    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.7!2d-74.0721!3d4.6588!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sBogot%C3%A1!5e0!3m2!1ses!2sco!4v1',

  /** A partir de este subtotal (COP) el envío estándar es gratis. */
  freeShippingThreshold: 300000,
} as const

/** Métodos de envío. Los `value` coinciden con las claves del backend. */
export const shippingOptions = [
  { value: 'estandar', label: 'Estándar', eta: '2 a 5 días hábiles', cost: 15000 },
  { value: 'express', label: 'Express', eta: '24 a 48 horas', cost: 30000 },
  { value: 'recoleccion', label: 'Recoge en tienda', eta: 'Hoy mismo', cost: 0 },
] as const

export type ShippingMethod = (typeof shippingOptions)[number]['value']

const currencyFormatter = new Intl.NumberFormat(site.locale, {
  style: 'currency',
  currency: site.currency,
  maximumFractionDigits: 0,
})

const numberFormatter = new Intl.NumberFormat(site.locale, {
  maximumFractionDigits: 0,
})

/** "$ 1.299.000" — con símbolo de moneda. */
export function formatCurrency(value: number | string): string {
  return currencyFormatter.format(Number(value) || 0)
}

/** "1.299.000" — solo el número agrupado (para plantillas que ya anteponen "$"). */
export function formatNumber(value: number | string): string {
  return numberFormatter.format(Number(value) || 0)
}

/** Mensaje de WhatsApp prellenado para consultar por un producto. */
export function whatsappProductUrl(productName: string, price: number | string): string {
  const text = encodeURIComponent(
    `¡Hola! Me interesa el ${productName} (${formatCurrency(price)}). ¿Me pueden dar más información?`,
  )
  return `https://wa.me/${site.whatsappNumber}?text=${text}`
}

export const whatsappUrl = `https://wa.me/${site.whatsappNumber}`
