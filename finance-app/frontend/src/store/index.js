import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Vues d'authentification
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'

// Vues principales
import Dashboard from '../views/Dashboard.vue'
import Analysis from '../views/analysis/Analysis.vue'
import Portfolio from '../views/portfolio/Portfolio.vue'
import Alerts from '../views/alerts/Alerts.vue'
import Calendar from '../views/Calendar.vue'
import Settings from '../views/Settings.vue'

// Vues d'analyse
import TechnicalAnalysis from '../views/analysis/TechnicalAnalysis.vue'
import IctAnalysis from '../views/analysis/IctAnalysis.vue'

// Vues de portefeuille
import PortfolioOverview from '../views/portfolio/PortfolioOverview.vue'
import PortfolioDetails from '../views/portfolio/PortfolioDetails.vue'
import AddTransaction from '../views/portfolio/AddTransaction.vue'

// Vues d'alertes
import AlertsList from '../views/alerts/AlertsList.vue'
import CreateAlert from '../views/alerts/CreateAlert.vue'

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
    path: '/analysis',
    name: 'Analysis',
    component: Analysis,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'technical/:symbol?',
        name: 'TechnicalAnalysis',
        component: TechnicalAnalysis,
        props: true
      },
      {
        path: 'ict/:symbol?',
        name: 'IctAnalysis',
        component: IctAnalysis,
        props: true
      }
    ]
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: Portfolio,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'PortfolioOverview',
        component: PortfolioOverview
      },
      {
        path: ':id',
        name: 'PortfolioDetails',
        component: PortfolioDetails,
        props: true
      },
      {
        path: ':id/transaction',
        name: 'AddTransaction',
        component: AddTransaction,
        props: true
      }
    ]
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'AlertsList',
        component: AlertsList
      },
      {
        path: 'create',
        name: 'CreateAlert',
        component: CreateAlert
      }
    ]
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

// Navigation guard
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
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
