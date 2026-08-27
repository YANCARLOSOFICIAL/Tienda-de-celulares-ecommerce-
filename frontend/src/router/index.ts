import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import { useAuthStore } from '@/stores/auth'

// Las vistas se cargan bajo demanda (code-splitting): el bundle inicial solo
// incluye la Home y el shell de la app.
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { title: 'Tienda Cell | Celulares, Reparación y Accesorios' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { title: 'Iniciar sesión | Tienda Cell', guestOnly: true }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('@/pages/ForgotPasswordPage.vue'),
    meta: { title: 'Recuperar contraseña | Tienda Cell', guestOnly: true }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: () => import('@/pages/ResetPasswordPage.vue'),
    meta: { title: 'Restablecer contraseña | Tienda Cell', guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/pages/RegisterPage.vue'),
    meta: { title: 'Crear cuenta | Tienda Cell', guestOnly: true }
  },
  {
    path: '/products/:id',
    name: 'product-detail',
    component: () => import('@/pages/ProductPage.vue'),
    meta: { title: 'Producto | Tienda Cell' }
  },
  {
    path: '/shop',
    name: 'shop',
    component: () => import('@/pages/ShopPage.vue'),
    meta: { title: 'Tienda | Tienda Cell' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('@/pages/ProfilePage.vue'),
    meta: { title: 'Mi perfil | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/wishlist',
    name: 'wishlist',
    component: () => import('@/pages/WishlistPage.vue'),
    meta: { title: 'Mis favoritos | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('@/pages/CartPage.vue'),
    meta: { title: 'Mi carrito | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: () => import('@/pages/CheckoutPage.vue'),
    meta: { title: 'Confirmar pedido | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'orders',
    component: () => import('@/pages/OrdersPage.vue'),
    meta: { title: 'Mis pedidos | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/orders/:id',
    name: 'order-detail',
    component: () => import('@/pages/OrderDetailPage.vue'),
    meta: { title: 'Detalle de pedido | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/compare',
    name: 'compare',
    component: () => import('@/pages/ComparePage.vue'),
    meta: { title: 'Comparar productos | Tienda Cell' }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/pages/AdminPage.vue'),
    meta: { title: 'Panel de administración | Tienda Cell', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: { title: 'Página no encontrada | Tienda Cell' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  if (!authStore.user) {
    await authStore.fetchMe()
  }

  document.title = (to.meta.title as string) || 'Tienda Cell'

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return { name: 'Home' }
  }
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'Home' }
  }
  return true
})

export default router
