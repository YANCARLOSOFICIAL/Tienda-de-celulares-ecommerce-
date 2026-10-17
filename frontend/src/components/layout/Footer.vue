<script setup lang="ts">
import { site, whatsappUrl } from '@/config/site'

const footerCols = [
  {
    heading: 'Tienda',
    links: [
      { label: 'Novedades', to: '/shop' },
      { label: 'Colecciones', to: '/shop' },
      { label: 'Comparar', to: '/compare' },
      { label: 'Favoritos', to: '/wishlist' },
    ],
  },
  {
    heading: 'Servicios',
    links: [
      { label: 'Asesoría privada', href: whatsappUrl },
      { label: 'Plan canje', href: whatsappUrl },
      { label: 'Garantía', href: whatsappUrl },
      { label: 'Localizador', href: whatsappUrl },
    ],
  },
  {
    heading: 'Casa',
    links: [
      { label: 'Nuestra historia', to: '/' },
      { label: 'Inner Circle', to: '/' },
      { label: 'Prensa', href: whatsappUrl },
      { label: 'Sostenibilidad', href: whatsappUrl },
    ],
  },
  {
    heading: 'Soporte',
    links: [
      { label: 'Contacto', href: whatsappUrl },
      { label: 'Envíos', href: whatsappUrl },
      { label: 'Devoluciones', href: whatsappUrl },
      { label: site.email, href: `mailto:${site.email}` },
    ],
  },
]
</script>

<template>
  <footer class="maison-footer border-t border-border" role="contentinfo">
    <div class="max-w-[1280px] mx-auto px-6 py-16">
      <div class="footer-top">
        <div class="footer-brand">
          <router-link to="/" class="footer-logo">
            TIENDA<span class="footer-logo-accent">CELL</span>
          </router-link>
          <p class="footer-tagline">
            Tecnología atemporal desde 2010. Bogotá · Medellín · Cali · Barranquilla
          </p>
        </div>

        <div class="footer-cols">
          <div v-for="col in footerCols" :key="col.heading" class="footer-col">
            <h3 class="footer-heading">{{ col.heading }}</h3>
            <ul>
              <li v-for="link in col.links" :key="link.label">
                <router-link v-if="link.to" :to="link.to" class="footer-link">
                  {{ link.label }}
                </router-link>
                <a
                  v-else
                  :href="link.href"
                  class="footer-link"
                  :target="link.href?.startsWith('http') ? '_blank' : undefined"
                  :rel="link.href?.startsWith('http') ? 'noopener noreferrer' : undefined"
                >
                  {{ link.label }}
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© {{ new Date().getFullYear() }} Tienda Cell. Todos los derechos reservados.</p>
        <div class="flex items-center gap-3">
          <a href="#" class="social-link" aria-label="Facebook">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="#" class="social-link" aria-label="Instagram">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
          </a>
          <a :href="`https://wa.me/${site.whatsappNumber}`" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="WhatsApp">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer-top {
  display: grid;
  gap: 48px;
  margin-bottom: 56px;
}

@media (min-width: 900px) {
  .footer-top {
    grid-template-columns: 1.2fr 2fr;
    gap: 80px;
  }
}

.footer-logo {
  font-family: var(--font-family-serif);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 0.22em;
  color: var(--color-text);
  text-decoration: none;
  display: inline-block;
  margin-bottom: 14px;
}

.footer-logo-accent {
  color: var(--color-accent);
}

.footer-tagline {
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text-tertiary);
  max-width: 280px;
}

.footer-cols {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 32px;
}

@media (min-width: 768px) {
  .footer-cols {
    grid-template-columns: repeat(4, 1fr);
  }
}

.footer-heading {
  font-family: var(--font-family-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--color-accent);
  margin-bottom: 18px;
}

.footer-col ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-link {
  font-size: 14px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.25s ease;
  cursor: pointer;
}

.footer-link:hover {
  color: var(--color-accent);
}

.footer-bottom {
  padding-top: 28px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

@media (min-width: 640px) {
  .footer-bottom {
    flex-direction: row;
  }
}

.footer-bottom p {
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--color-text-tertiary);
}

.social-link {
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
  transition: all 0.3s ease;
}

.social-link:hover {
  color: var(--color-accent);
  border-color: rgba(240, 196, 25, 0.4);
  background: rgba(240, 196, 25, 0.06);
}
</style>
