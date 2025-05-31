import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../Dashboard.vue'
import Portfolio from '../Portfolio.vue'
import Alerts from '../Alerts.vue'
import Settings from '../Settings.vue'
import Calendar from '../Calendar.vue'
import TechnicalAnalysis from '../TechnicalAnalysis.vue'
import Login from '../Login.vue'
import Register from '../Register.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/portfolio',
    name: 'Portfolio',
    component: Portfolio
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar
  },
  {
    path: '/analysis/technical',
    name: 'TechnicalAnalysis',
    component: TechnicalAnalysis
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
