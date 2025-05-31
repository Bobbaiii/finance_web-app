import axios from 'axios'
import jwtDecode from 'jwt-decode'

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
    token: localStorage.getItem('token') || null,
    user: null
  },
  getters: {
    isAuthenticated: state => !!state.token,
    getUser: state => state.user,
    getToken: state => state.token
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    SET_USER(state, user) {
      state.user = user
    },
    CLEAR_AUTH(state) {
      state.token = null
      state.user = null
      localStorage.removeItem('token')
    }
  },
  actions: {
    async register({ commit, dispatch }, credentials) {
      try {
        const response = await api.post('/users/register', credentials)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de l\'inscription', { root: true })
        throw error
      }
    },
    async login({ commit, dispatch }, credentials) {
      try {
        // Conversion des données au format attendu par l'API
        const formData = new FormData()
        formData.append('username', credentials.email)
        formData.append('password', credentials.password)
        
        const response = await api.post('/users/login', formData)
        const { access_token } = response.data
        
        commit('SET_TOKEN', access_token)
        await dispatch('fetchUserProfile')
        
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la connexion', { root: true })
        throw error
      }
    },
    async fetchUserProfile({ commit, state, dispatch }) {
      try {
        if (!state.token) return null
        
        const response = await api.get('/users/me')
        commit('SET_USER', response.data)
        return response.data
      } catch (error) {
        if (error.response && error.response.status === 401) {
          // Token expiré ou invalide
          commit('CLEAR_AUTH')
        }
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération du profil', { root: true })
        throw error
      }
    },
    logout({ commit }) {
      commit('CLEAR_AUTH')
    },
    async updateNotificationSettings({ commit, dispatch }, settings) {
      try {
        const response = await api.put('/users/notification-settings', settings)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la mise à jour des paramètres de notification', { root: true })
        throw error
      }
    },
    async getNotificationSettings({ dispatch }) {
      try {
        const response = await api.get('/users/notification-settings')
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des paramètres de notification', { root: true })
        throw error
      }
    },
    checkTokenExpiration({ state, commit }) {
      if (!state.token) return false
      
      try {
        const decoded = jwtDecode(state.token)
        const currentTime = Date.now() / 1000
        
        if (decoded.exp < currentTime) {
          // Token expiré
          commit('CLEAR_AUTH')
          return false
        }
        
        return true
      } catch (error) {
        // Token invalide
        commit('CLEAR_AUTH')
        return false
      }
    }
  }
}
