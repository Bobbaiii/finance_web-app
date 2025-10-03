import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import TechnicalAnalysis from '../views/TechnicalAnalysis.vue'
import Portfolio from '../views/Portfolio.vue'
import Alerts from '../views/Alerts.vue'
import Calendar from '../Calendar.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis/technical/:symbol?',
    name: 'TechnicalAnalysis',
    component: TechnicalAnalysis,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/analysis/ict/:symbol?',
    name: 'IctAnalysis',
    component: TechnicalAnalysis,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: Portfolio,
    meta: { requiresAuth: true }
  },
  {
    path: '/portfolio/:id',
    name: 'PortfolioDetails',
    component: Portfolio,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/portfolio/:id/transaction',
    name: 'AddTransaction',
    component: Portfolio,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts,
    meta: { requiresAuth: true }
  },
  {
    path: '/alerts/create',
    name: 'CreateAlert',
    component: Alerts,
    meta: { requiresAuth: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta?.requiresAuth)
  const isAuthenticated = store.getters['auth/isAuthenticated']

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (!requiresAuth && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
