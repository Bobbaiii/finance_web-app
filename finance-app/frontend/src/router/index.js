import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Portfolio from '../views/Portfolio.vue'
import Alerts from '../views/Alerts.vue'
import Settings from '../views/Settings.vue'
import Calendar from '../views/Calendar.vue'
import TechnicalAnalysis from '../views/TechnicalAnalysis.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

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
