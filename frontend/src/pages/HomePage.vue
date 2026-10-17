<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ArrowRight, Check, Menu, X, ShoppingCart, User } from '@lucide/vue'
import { formatCurrency, whatsappUrl } from '@/config/site'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const authStore = useAuthStore()
const cartStore = useCartStore()

/* ── Nav ── */
const isScrolled = ref(false)
const isMenuOpen = ref(false)

const navLinks = [
  { label: 'Colección', href: '#featured' },
  { label: 'Herencia', href: '#heritage' },
  { label: 'Colecciones', href: '#collections' },
  { label: 'Inner Circle', href: '#membership' },
]

function handleScroll() {
  isScrolled.value = window.scrollY > 40
}

function scrollTo(id: string) {
  isMenuOpen.value = false
  const el = document.querySelector(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

/* ── Reveal ── */
let observer: IntersectionObserver | null = null

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
  if (!authStore.user) await authStore.fetchMe()
  if (authStore.isAuthenticated) await cartStore.fetchCart()
  const els = Array.from(document.querySelectorAll<HTMLElement>('[data-reveal]'))
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    els.forEach((el) => el.classList.add('is-visible'))
    return
  }
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
          observer?.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.12, rootMargin: '0px 0px -30px 0px' },
  )
  els.forEach((el) => observer?.observe(el))
})

onUnmounted(() => {
  observer?.disconnect()
  window.removeEventListener('scroll', handleScroll)
})

/* ── Datos ── */
const stats = [
  { value: '150+', label: 'Piezas exclusivas' },
  { value: '48', label: 'Boutiques aliadas' },
  { value: '2010', label: 'Est. Bogotá' },
]

const products = [
  {
    id: 1,
    name: 'iPhone 16 Pro Max',
    price: 6499000,
    badge: 'Nuevo',
    image:
      'https://images.unsplash.com/photo-1695048133142-1e20484d2569?w=600&h=800&fit=crop&q=80',
    alt: 'iPhone 16 Pro Max titanio',
  },
  {
    id: 2,
    name: 'Galaxy S25 Ultra',
    price: 5999000,
    badge: null,
    image:
      'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600&h=800&fit=crop&q=80',
    alt: 'Samsung Galaxy S25 Ultra',
  },
  {
    id: 3,
    name: 'Xiaomi 15 Ultra',
    price: 4299000,
    badge: 'Exclusivo',
    image:
      'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&h=800&fit=crop&q=80',
    alt: 'Xiaomi 15 Ultra Leica',
  },
  {
    id: 4,
    name: 'Audio Master Pro',
    price: 1899000,
    badge: null,
    image:
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=800&fit=crop&q=80',
    alt: 'Audífonos premium Audio Master Pro',
  },
]

const pillars = [
  { title: 'Calidad', desc: 'Estándares irreprochables' },
  { title: 'Pasión', desc: 'Dedicación de artesanos' },
  { title: 'Atemporal', desc: 'Diseño que perdura' },
]

const collections = [
  {
    title: 'Smartphones',
    subtitle: 'La cúspide móvil',
    image:
      'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=600&fit=crop&q=80',
  },
  {
    title: 'Audio',
    subtitle: 'Sonido de concierto',
    image:
      'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&h=600&fit=crop&q=80',
  },
  {
    title: 'Wearables',
    subtitle: 'Tecnología al pulso',
    image:
      'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&h=600&fit=crop&q=80',
  },
]

const perks = [
  'Acceso anticipado a lanzamientos limitados',
  'Invitaciones a eventos privados',
  'Envoltorio de regalo de cortesía',
  'Asesor de estilo tecnológico personal',
]

const email = ref('')
const subscribed = ref(false)

function subscribe() {
  if (!email.value) return
  subscribed.value = true
  email.value = ''
}
</script>

<template>
  <div class="maison">
    <!-- ═══════════ NAV ═══════════ -->
    <header :class="['maison-nav', { scrolled: isScrolled }]">
      <nav class="nav-inner" aria-label="Navegación principal">
        <a href="#top" class="nav-logo" @click.prevent="scrollTo('#top')">
          TIENDA<span class="nav-logo-accent">CELL</span>
        </a>

        <div class="nav-links">
          <a
            v-for="link in navLinks"
            :key="link.label"
            :href="link.href"
            class="nav-link"
            @click.prevent="scrollTo(link.href)"
          >
            {{ link.label }}
          </a>
        </div>

        <div class="nav-actions">
          <RouterLink to="/shop" class="nav-shop-link">Tienda</RouterLink>

          <RouterLink to="/cart" class="nav-icon" aria-label="Ver carrito">
            <ShoppingCart :size="18" :stroke-width="1.5" />
            <span v-if="cartStore.itemCount > 0" class="nav-badge">{{ cartStore.itemCount }}</span>
          </RouterLink>

          <RouterLink
            v-if="!authStore.isAuthenticated"
            to="/login"
            class="nav-icon"
            aria-label="Iniciar sesión"
          >
            <User :size="18" :stroke-width="1.5" />
          </RouterLink>

          <button
            class="nav-icon nav-burger lg:hidden"
            :aria-label="isMenuOpen ? 'Cerrar menú' : 'Abrir menú'"
            :aria-expanded="isMenuOpen"
            @click="isMenuOpen = !isMenuOpen"
          >
            <Menu v-if="!isMenuOpen" :size="20" :stroke-width="1.5" />
            <X v-else :size="20" :stroke-width="1.5" />
          </button>
        </div>
      </nav>

      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-show="isMenuOpen" class="nav-mobile">
          <a
            v-for="link in navLinks"
            :key="link.label"
            :href="link.href"
            class="nav-mobile-link"
            @click.prevent="scrollTo(link.href)"
          >
            {{ link.label }}
          </a>
          <RouterLink to="/shop" class="nav-mobile-link" @click="isMenuOpen = false">
            Tienda
          </RouterLink>
        </div>
      </Transition>
    </header>

    <!-- ═══════════ HERO ═══════════ -->
    <section id="top" class="hero">
      <div class="hero-media" aria-hidden="true">
        <img
          src="https://images.unsplash.com/photo-1556656793-08538906a9f8?w=1920&h=1080&fit=crop&q=80"
          alt=""
          class="hero-img"
          width="1920"
          height="1080"
          fetchpriority="high"
        />
        <div class="hero-overlay"></div>
      </div>

      <div class="hero-content">
        <p class="eyebrow-line" data-reveal>Colección Privée · 2026</p>
        <h1 class="hero-title" data-reveal>
          El arte de la<br />
          <span class="hero-title-accent">tecnología eterna</span>
        </h1>
        <p class="hero-sub" data-reveal>
          Descubre nuestra colección curada de dispositivos excepcionales,
          elaborados con atención inquebrantable al detalle.
        </p>
        <div class="hero-ctas" data-reveal>
          <a href="#featured" class="btn-fill" @click.prevent="scrollTo('#featured')">
            Explorar colección
            <ArrowRight :size="16" />
          </a>
          <a :href="whatsappUrl" target="_blank" rel="noopener" class="btn-outline">
            Reservar cita
          </a>
        </div>
      </div>

      <div class="hero-stats" data-reveal>
        <div v-for="s in stats" :key="s.label" class="stat">
          <span class="stat-value">{{ s.value }}</span>
          <span class="stat-label">{{ s.label }}</span>
        </div>
      </div>
    </section>

    <!-- ═══════════ FEATURED ═══════════ -->
    <section id="featured" class="section">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow-line">Selección curada</p>
          <h2 class="section-title">Piezas destacadas</h2>
        </div>

        <div class="product-grid">
          <article
            v-for="(p, i) in products"
            :key="p.id"
            class="product-card"
            :style="{ transitionDelay: `${i * 70}ms` }"
            data-reveal
          >
            <RouterLink :to="`/products/${p.id}`" class="product-media">
              <img
                :src="p.image"
                :alt="p.alt"
                loading="lazy"
                width="600"
                height="800"
                class="product-img"
              />
              <span v-if="p.badge" class="product-badge">{{ p.badge }}</span>
              <span class="product-quick">Vista rápida</span>
            </RouterLink>
            <div class="product-info">
              <h3 class="product-name">
                <RouterLink :to="`/products/${p.id}`">{{ p.name }}</RouterLink>
              </h3>
              <p class="product-price">{{ formatCurrency(p.price) }}</p>
            </div>
          </article>
        </div>

        <div class="section-cta" data-reveal>
          <RouterLink to="/shop" class="btn-outline">
            Ver todos los productos
            <ArrowRight :size="15" />
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ═══════════ HERITAGE ═══════════ -->
    <section id="heritage" class="section heritage">
      <div class="container heritage-grid">
        <div class="heritage-visual" data-reveal>
          <img
            src="https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800&h=1000&fit=crop&q=80"
            alt="Artesanía en tecnología premium"
            loading="lazy"
            width="800"
            height="1000"
            class="heritage-img"
          />
          <div class="heritage-stat">
            <span class="heritage-stat-num">15+</span>
            <span class="heritage-stat-label">Años de excelencia</span>
          </div>
        </div>

        <div class="heritage-copy" data-reveal>
          <p class="eyebrow-line">Nuestra herencia</p>
          <h2 class="section-title heritage-title">
            Un legado de<br />artesanía
          </h2>
          <p class="body-text">
            Desde 2010, Tienda Cell es sinónimo de calidad excepcional y diseño atemporal.
            Nuestros especialistas continúan técnicas de curaduría de décadas, fusionando
            tradición con visión contemporánea.
          </p>
          <p class="body-text">
            Cada dispositivo de nuestra colección cuenta una historia: de artesanía meticulosa,
            de materiales raros y de un compromiso inquebrantable con la excelencia.
          </p>

          <div class="pillars">
            <div v-for="p in pillars" :key="p.title" class="pillar">
              <h3 class="pillar-title">{{ p.title }}</h3>
              <p class="pillar-desc">{{ p.desc }}</p>
            </div>
          </div>

          <a href="#collections" class="btn-outline" @click.prevent="scrollTo('#collections')">
            Descubrir nuestra historia
            <ArrowRight :size="15" />
          </a>
        </div>
      </div>
    </section>

    <!-- ═══════════ COLLECTIONS ═══════════ -->
    <section id="collections" class="section">
      <div class="container">
        <div class="section-head" data-reveal>
          <p class="eyebrow-line">Explorar</p>
          <h2 class="section-title">Nuestras colecciones</h2>
        </div>

        <div class="collection-grid">
          <RouterLink
            v-for="(c, i) in collections"
            :key="c.title"
            to="/shop"
            class="collection-card"
            :style="{ transitionDelay: `${i * 80}ms` }"
            data-reveal
          >
            <img
              :src="c.image"
              :alt="c.title"
              loading="lazy"
              width="800"
              height="600"
              class="collection-img"
            />
            <div class="collection-overlay">
              <h3 class="collection-title">{{ c.title }}</h3>
              <p class="collection-sub">{{ c.subtitle }}</p>
              <span class="collection-explore">
                Explorar
                <ArrowRight :size="14" />
              </span>
            </div>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- ═══════════ INNER CIRCLE ═══════════ -->
    <section id="membership" class="section membership">
      <div class="container membership-grid">
        <div class="membership-copy" data-reveal>
          <p class="eyebrow-line">Acceso exclusivo</p>
          <h2 class="section-title membership-title">
            Únete al<br /><span class="hero-title-accent">Inner Circle</span>
          </h2>
          <p class="body-text">
            Conviértete en miembro y desbloquea beneficios exclusivos: acceso anticipado
            a nuevas colecciones, eventos privados, consultas de estilo personal y
            grabación de regalos de cortesía.
          </p>

          <ul class="perks">
            <li v-for="perk in perks" :key="perk" class="perk">
              <span class="perk-check" aria-hidden="true">
                <Check :size="12" :stroke-width="2.5" />
              </span>
              {{ perk }}
            </li>
          </ul>

          <a
            :href="whatsappUrl"
            target="_blank"
            rel="noopener"
            class="btn-fill"
          >
            Solicitar membresía
            <ArrowRight :size="16" />
          </a>
        </div>

        <div class="membership-visual" data-reveal>
          <img
            src="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=600&h=800&fit=crop&q=80"
            alt="Experiencia Inner Circle"
            loading="lazy"
            width="600"
            height="800"
            class="membership-img"
          />
          <span class="vip-badge">VIP</span>
        </div>
      </div>
    </section>

    <!-- ═══════════ NEWSLETTER ═══════════ -->
    <section class="section newsletter">
      <div class="container newsletter-inner" data-reveal>
        <div class="newsletter-copy">
          <p class="eyebrow-line">Mantente cerca</p>
          <h2 class="section-title newsletter-title">Suscríbete a nuestro círculo</h2>
          <p class="body-text">
            Recibe novedades, ofertas exclusivas y consejos de estilo tecnológico.
          </p>
        </div>
        <form class="newsletter-form" @submit.prevent="subscribe">
          <label for="newsletter-email" class="sr-only">Correo electrónico</label>
          <input
            id="newsletter-email"
            v-model="email"
            type="email"
            required
            placeholder="tu@correo.com"
            class="newsletter-input"
            autocomplete="email"
          />
          <button type="submit" class="btn-fill newsletter-btn">
            {{ subscribed ? '¡Listo!' : 'Suscribirme' }}
            <Check v-if="subscribed" :size="16" />
            <ArrowRight v-else :size="16" />
          </button>
        </form>
      </div>
    </section>

    <!-- ═══════════ FOOTER ═══════════ -->
    <footer class="maison-footer" role="contentinfo">
      <div class="container">
        <div class="footer-top">
          <div class="footer-brand">
            <p class="footer-logo">TIENDA<span class="nav-logo-accent">CELL</span></p>
            <p class="footer-tagline">
              Tecnología atemporal desde 2010. Bogotá · Medellín · Cali · Barranquilla
            </p>
          </div>

          <div class="footer-cols">
            <div class="footer-col">
              <h3 class="footer-heading">Tienda</h3>
              <ul>
                <li><RouterLink to="/shop" class="footer-link">Novedades</RouterLink></li>
                <li><a href="#collections" class="footer-link" @click.prevent="scrollTo('#collections')">Colecciones</a></li>
                <li><RouterLink to="/shop" class="footer-link">Accesorios</RouterLink></li>
                <li><RouterLink to="/compare" class="footer-link">Comparar</RouterLink></li>
              </ul>
            </div>
            <div class="footer-col">
              <h3 class="footer-heading">Servicios</h3>
              <ul>
                <li><a href="#servicios" class="footer-link" @click.prevent="scrollTo('#heritage')">Asesoría privada</a></li>
                <li><RouterLink to="/shop" class="footer-link">Plan canje</RouterLink></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Garantía</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Localizador</a></li>
              </ul>
            </div>
            <div class="footer-col">
              <h3 class="footer-heading">Casa</h3>
              <ul>
                <li><a href="#heritage" class="footer-link" @click.prevent="scrollTo('#heritage')">Nuestra historia</a></li>
                <li><a href="#membership" class="footer-link" @click.prevent="scrollTo('#membership')">Inner Circle</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Prensa</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Sostenibilidad</a></li>
              </ul>
            </div>
            <div class="footer-col">
              <h3 class="footer-heading">Soporte</h3>
              <ul>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Contacto</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Envíos</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">Devoluciones</a></li>
                <li><a :href="whatsappUrl" target="_blank" rel="noopener" class="footer-link">FAQ</a></li>
              </ul>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} Tienda Cell. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* ═══════════ TOKENS EDITORIALES ═══════════ */
.maison {
  --ink: #0a0906;
  --ink-soft: #12100a;
  --cream: #f5f0e6;
  --cream-dim: #c4bba8;
  --cream-faint: #8a8272;
  --yellow: #f0c419;
  --mustard: #c9a227;
  --line: rgba(245, 240, 230, 0.12);

  background: var(--ink);
  color: var(--cream);
  min-height: 100vh;
}

/* ═══════════ NAV ═══════════ */
.maison-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  transition: background 0.4s ease, border-color 0.4s ease;
  border-bottom: 1px solid transparent;
}

.maison-nav.scrolled {
  background: rgba(10, 9, 6, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom-color: var(--line);
}

.nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.nav-logo {
  font-family: var(--font-family-serif);
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.22em;
  color: var(--cream);
  text-decoration: none;
}

.nav-logo-accent {
  color: var(--yellow);
  margin-left: 2px;
}

.nav-links {
  display: none;
  align-items: center;
  gap: 32px;
}

@media (min-width: 1024px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--cream-dim);
  text-decoration: none;
  transition: color 0.25s ease;
  cursor: pointer;
}

.nav-link:hover {
  color: var(--yellow);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-shop-link {
  display: none;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--cream);
  text-decoration: none;
  padding: 8px 0;
  margin-right: 8px;
  border-bottom: 1px solid var(--yellow);
  transition: color 0.25s ease;
  cursor: pointer;
}

@media (min-width: 640px) {
  .nav-shop-link {
    display: inline;
  }
}

.nav-shop-link:hover {
  color: var(--yellow);
}

.nav-icon {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--cream-dim);
  border-radius: 50%;
  transition: color 0.25s ease, background 0.25s ease;
  cursor: pointer;
  text-decoration: none;
}

.nav-icon:hover {
  color: var(--yellow);
  background: rgba(240, 196, 25, 0.08);
}

.nav-badge {
  position: absolute;
  top: 4px;
  right: 2px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 999px;
  background: var(--yellow);
  color: var(--ink);
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.nav-burger {
  display: inline-flex;
}

@media (min-width: 1024px) {
  .nav-burger {
    display: none;
  }
}

.nav-mobile {
  display: flex;
  flex-direction: column;
  padding: 8px 24px 24px;
  background: rgba(10, 9, 6, 0.97);
  border-bottom: 1px solid var(--line);
}

@media (min-width: 1024px) {
  .nav-mobile {
    display: none;
  }
}

.nav-mobile-link {
  padding: 14px 0;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--cream-dim);
  text-decoration: none;
  border-bottom: 1px solid var(--line);
  cursor: pointer;
  transition: color 0.2s ease;
}

.nav-mobile-link:hover {
  color: var(--yellow);
}

/* ═══════════ HERO ═══════════ */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 120px 0 0;
}

.hero-media {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 30%;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(10, 9, 6, 0.55) 0%, rgba(10, 9, 6, 0.25) 40%, rgba(10, 9, 6, 0.92) 100%),
    linear-gradient(90deg, rgba(10, 9, 6, 0.7) 0%, transparent 60%);
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.eyebrow-line {
  font-family: var(--font-family-mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: var(--yellow);
  margin-bottom: 20px;
}

.hero-title {
  font-family: var(--font-family-serif);
  font-size: clamp(44px, 8vw, 88px);
  font-weight: 500;
  line-height: 1.02;
  letter-spacing: -0.02em;
  color: var(--cream);
  margin-bottom: 24px;
}

.hero-title-accent {
  color: var(--yellow);
}

.hero-sub {
  max-width: 480px;
  font-size: clamp(15px, 1.5vw, 17px);
  line-height: 1.7;
  color: var(--cream-dim);
  margin-bottom: 36px;
}

.hero-ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

/* Botones maison */
.btn-fill {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 15px 28px;
  background: var(--yellow);
  color: var(--ink);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-decoration: none;
  border: none;
  border-radius: 0;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.3s ease;
}

.btn-fill:hover {
  background: var(--mustard);
  transform: translateY(-1px);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;
  background: transparent;
  color: var(--cream);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  text-decoration: none;
  border: 1px solid rgba(245, 240, 230, 0.35);
  border-radius: 0;
  cursor: pointer;
  transition: border-color 0.3s ease, color 0.3s ease, background 0.3s ease;
}

.btn-outline:hover {
  border-color: var(--yellow);
  color: var(--yellow);
  background: rgba(240, 196, 25, 0.05);
}

/* Stats bar */
.hero-stats {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 24px;
  border-top: 1px solid rgba(245, 240, 230, 0.15);
  background: rgba(10, 9, 6, 0.35);
  backdrop-filter: blur(12px);
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  text-align: center;
}

.stat-value {
  font-family: var(--font-family-serif);
  font-size: clamp(26px, 3.5vw, 36px);
  font-weight: 500;
  color: var(--cream);
  line-height: 1.1;
}

.stat-label {
  font-size: 12px;
  letter-spacing: 0.06em;
  color: var(--cream-faint);
}

/* ═══════════ SECCIONES ═══════════ */
.section {
  padding: clamp(80px, 12vw, 140px) 0;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-head {
  margin-bottom: clamp(40px, 6vw, 64px);
}

.section-title {
  font-family: var(--font-family-serif);
  font-size: clamp(32px, 5vw, 52px);
  font-weight: 500;
  line-height: 1.1;
  letter-spacing: -0.015em;
  color: var(--cream);
}

.body-text {
  font-size: 15.5px;
  line-height: 1.75;
  color: var(--cream-dim);
  margin-bottom: 18px;
  max-width: 520px;
}

.section-cta {
  margin-top: 48px;
  text-align: center;
}

/* ═══════════ PRODUCTS ═══════════ */
.product-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px 16px;
}

@media (min-width: 900px) {
  .product-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 32px 24px;
  }
}

.product-card {
  display: flex;
  flex-direction: column;
}

.product-media {
  position: relative;
  display: block;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  background: var(--ink-soft);
  text-decoration: none;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.product-card:hover .product-img {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  padding: 5px 12px;
  background: var(--yellow);
  color: var(--ink);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  z-index: 2;
}

.product-quick {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 14px;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--cream);
  background: rgba(10, 9, 6, 0.78);
  backdrop-filter: blur(8px);
  transform: translateY(100%);
  transition: transform 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.product-card:hover .product-quick {
  transform: translateY(0);
}

.product-info {
  padding-top: 16px;
}

.product-name {
  font-family: var(--font-family-serif);
  font-size: 17px;
  font-weight: 500;
  margin-bottom: 6px;
}

.product-name a {
  color: var(--cream);
  text-decoration: none;
  transition: color 0.25s ease;
}

.product-name a:hover {
  color: var(--yellow);
}

.product-price {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
  color: var(--cream-dim);
}

/* ═══════════ HERITAGE ═══════════ */
.heritage {
  background: var(--ink-soft);
}

.heritage-grid {
  display: grid;
  gap: 48px;
  align-items: center;
}

@media (min-width: 900px) {
  .heritage-grid {
    grid-template-columns: 1fr 1fr;
    gap: 80px;
  }
}

.heritage-visual {
  position: relative;
}

.heritage-img {
  width: 100%;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  display: block;
}

.heritage-stat {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 28px 24px;
  background: linear-gradient(180deg, transparent, rgba(10, 9, 6, 0.9));
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.heritage-stat-num {
  font-family: var(--font-family-serif);
  font-size: clamp(36px, 5vw, 48px);
  font-weight: 500;
  color: var(--yellow);
  line-height: 1;
}

.heritage-stat-label {
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--cream-dim);
}

.heritage-title {
  margin-bottom: 24px;
}

.pillars {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin: 36px 0 40px;
  padding-top: 32px;
  border-top: 1px solid var(--line);
}

.pillar-title {
  font-family: var(--font-family-serif);
  font-size: 16px;
  font-weight: 500;
  color: var(--cream);
  margin-bottom: 6px;
}

.pillar-desc {
  font-size: 13px;
  color: var(--cream-faint);
  line-height: 1.5;
}

/* ═══════════ COLLECTIONS ═══════════ */
.collection-grid {
  display: grid;
  gap: 16px;
}

@media (min-width: 768px) {
  .collection-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }
}

.collection-card {
  position: relative;
  display: block;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  text-decoration: none;
  background: var(--ink-soft);
}

@media (min-width: 768px) {
  .collection-card {
    aspect-ratio: 4 / 5;
  }
}

.collection-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}

.collection-card:hover .collection-img {
  transform: scale(1.06);
}

.collection-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 28px;
  background: linear-gradient(180deg, transparent 40%, rgba(10, 9, 6, 0.88) 100%);
}

.collection-title {
  font-family: var(--font-family-serif);
  font-size: 24px;
  font-weight: 500;
  color: var(--cream);
  margin-bottom: 4px;
}

.collection-sub {
  font-size: 13px;
  color: var(--cream-dim);
  margin-bottom: 14px;
}

.collection-explore {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--yellow);
  transition: gap 0.3s ease;
}

.collection-card:hover .collection-explore {
  gap: 14px;
}

/* ═══════════ MEMBERSHIP ═══════════ */
.membership {
  background: var(--ink-soft);
}

.membership-grid {
  display: grid;
  gap: 48px;
  align-items: center;
}

@media (min-width: 900px) {
  .membership-grid {
    grid-template-columns: 1.1fr 0.9fr;
    gap: 80px;
  }
}

.membership-title {
  margin-bottom: 20px;
}

.perks {
  list-style: none;
  margin: 0 0 36px;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.perk {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 15px;
  color: var(--cream-dim);
}

.perk-check {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--yellow);
  color: var(--yellow);
}

.membership-visual {
  position: relative;
}

.membership-img {
  width: 100%;
  aspect-ratio: 3 / 4;
  object-fit: cover;
  display: block;
}

.vip-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 18px;
  background: var(--yellow);
  color: var(--ink);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.2em;
}

/* ═══════════ NEWSLETTER ═══════════ */
.newsletter-inner {
  display: grid;
  gap: 36px;
  align-items: end;
  padding-top: 48px;
  border-top: 1px solid var(--line);
}

@media (min-width: 768px) {
  .newsletter-inner {
    grid-template-columns: 1fr 1fr;
    gap: 64px;
  }
}

.newsletter-title {
  margin-bottom: 12px;
}

.newsletter-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 480px) {
  .newsletter-form {
    flex-direction: row;
  }
}

.newsletter-input {
  flex: 1;
  padding: 15px 18px;
  background: transparent;
  border: 1px solid rgba(245, 240, 230, 0.25);
  border-radius: 0;
  color: var(--cream);
  font-size: 15px;
  font-family: var(--font-family-sans);
  outline: none;
  transition: border-color 0.3s ease;
}

.newsletter-input::placeholder {
  color: var(--cream-faint);
}

.newsletter-input:focus {
  border-color: var(--yellow);
}

.newsletter-btn {
  white-space: nowrap;
  justify-content: center;
}

/* ═══════════ FOOTER ═══════════ */
.maison-footer {
  border-top: 1px solid var(--line);
  padding: 64px 0 32px;
  background: var(--ink);
}

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
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.22em;
  color: var(--cream);
  margin-bottom: 14px;
}

.footer-tagline {
  font-size: 14px;
  line-height: 1.7;
  color: var(--cream-faint);
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
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--yellow);
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
  color: var(--cream-dim);
  text-decoration: none;
  transition: color 0.25s ease;
  cursor: pointer;
}

.footer-link:hover {
  color: var(--yellow);
}

.footer-bottom {
  padding-top: 28px;
  border-top: 1px solid var(--line);
  text-align: center;
}

.footer-bottom p {
  font-size: 12px;
  letter-spacing: 0.04em;
  color: var(--cream-faint);
}

/* ═══════════ REVEAL ═══════════ */
[data-reveal] {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.6s cubic-bezier(0.23, 1, 0.32, 1), transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
}

[data-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  [data-reveal] {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }

  .product-img,
  .collection-img {
    transition: none;
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>
