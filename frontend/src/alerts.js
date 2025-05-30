import axios from 'axios'

// Création d'une instance axios avec l'URL de base
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1'
})

// Intercepteur pour ajouter le token d'authentification aux requêtes
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default {
  namespaced: true,
  state: {
    alerts: [],
    currentAlert: null,
    notificationSettings: null
  },
  getters: {
    getAlerts: state => state.alerts,
    getCurrentAlert: state => state.currentAlert,
    getNotificationSettings: state => state.notificationSettings
  },
  mutations: {
    SET_ALERTS(state, alerts) {
      state.alerts = alerts
    },
    SET_CURRENT_ALERT(state, alert) {
      state.currentAlert = alert
    },
    SET_NOTIFICATION_SETTINGS(state, settings) {
      state.notificationSettings = settings
    },
    ADD_ALERT(state, alert) {
      state.alerts.push(alert)
    },
    UPDATE_ALERT(state, updatedAlert) {
      const index = state.alerts.findIndex(a => a.id === updatedAlert.id)
      if (index !== -1) {
        state.alerts.splice(index, 1, updatedAlert)
      }
      if (state.currentAlert && state.currentAlert.id === updatedAlert.id) {
        state.currentAlert = updatedAlert
      }
    },
    REMOVE_ALERT(state, alertId) {
      state.alerts = state.alerts.filter(a => a.id !== alertId)
      if (state.currentAlert && state.currentAlert.id === alertId) {
        state.currentAlert = null
      }
    }
  },
  actions: {
    async fetchAlerts({ commit, dispatch }) {
      try {
        const response = await api.get('/alerts')
        commit('SET_ALERTS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des alertes', { root: true })
        throw error
      }
    },
    async fetchAlert({ commit, dispatch }, alertId) {
      try {
        const response = await api.get(`/alerts/${alertId}`)
        commit('SET_CURRENT_ALERT', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération de l\'alerte', { root: true })
        throw error
      }
    },
    async createAlert({ commit, dispatch }, alertData) {
      try {
        const response = await api.post('/alerts', alertData)
        commit('ADD_ALERT', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la création de l\'alerte', { root: true })
        throw error
      }
    },
    async updateAlert({ commit, dispatch }, { alertId, alertData }) {
      try {
        const response = await api.put(`/alerts/${alertId}`, alertData)
        commit('UPDATE_ALERT', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la mise à jour de l\'alerte', { root: true })
        throw error
      }
    },
    async deleteAlert({ commit, dispatch }, alertId) {
      try {
        await api.delete(`/alerts/${alertId}`)
        commit('REMOVE_ALERT', alertId)
        return { success: true }
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la suppression de l\'alerte', { root: true })
        throw error
      }
    },
    async fetchNotificationSettings({ commit, dispatch }) {
      try {
        const response = await api.get('/users/notification-settings')
        commit('SET_NOTIFICATION_SETTINGS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des paramètres de notification', { root: true })
        throw error
      }
    },
    async updateNotificationSettings({ commit, dispatch }, settings) {
      try {
        const response = await api.put('/users/notification-settings', settings)
        commit('SET_NOTIFICATION_SETTINGS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la mise à jour des paramètres de notification', { root: true })
        throw error
      }
    }
  }
}
