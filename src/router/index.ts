import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import CartPage from '../pages/CartPage.vue'
import CheckoutPage from '../pages/CheckoutPage.vue'
import OrdersPage from '../pages/OrdersPage.vue'
import OrderDetailPage from '../pages/OrderDetailPage.vue'
import AdminPage from '../pages/AdminPage.vue'
import ProductPage from '../pages/ProductPage.vue'
import ShopPage from '../pages/ShopPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import WishlistPage from '../pages/WishlistPage.vue'
import ForgotPasswordPage from '../pages/ForgotPasswordPage.vue'
import ResetPasswordPage from '../pages/ResetPasswordPage.vue'
import { useAuthStore } from '../stores/auth'

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
    component: LoginPage,
    meta: { title: 'Iniciar sesión | Tienda Cell', guestOnly: true }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: ForgotPasswordPage,
    meta: { title: 'Recuperar contraseña | Tienda Cell', guestOnly: true }
  },
  {
    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordPage,
    meta: { title: 'Restablecer contraseña | Tienda Cell', guestOnly: true }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage,
    meta: { title: 'Crear cuenta | Tienda Cell', guestOnly: true }
  },
  {
    path: '/products/:id',
    name: 'product-detail',
    component: ProductPage,
    meta: { title: 'Producto | Tienda Cell' }
  },
  {
    path: '/shop',
    name: 'shop',
    component: ShopPage,
    meta: { title: 'Tienda | Tienda Cell' }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfilePage,
    meta: { title: 'Mi perfil | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/wishlist',
    name: 'wishlist',
    component: WishlistPage,
    meta: { title: 'Mis favoritos | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartPage,
    meta: { title: 'Mi carrito | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: CheckoutPage,
    meta: { title: 'Confirmar pedido | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'orders',
    component: OrdersPage,
    meta: { title: 'Mis pedidos | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/orders/:id',
    name: 'order-detail',
    component: OrderDetailPage,
    meta: { title: 'Detalle de pedido | Tienda Cell', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPage,
    meta: { title: 'Panel de administración | Tienda Cell', requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
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
