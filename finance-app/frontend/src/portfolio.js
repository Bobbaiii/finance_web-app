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
    portfolios: [],
    currentPortfolio: null,
    transactions: [],
    performance: null
  },
  getters: {
    getPortfolios: state => state.portfolios,
    getCurrentPortfolio: state => state.currentPortfolio,
    getTransactions: state => state.transactions,
    getPerformance: state => state.performance
  },
  mutations: {
    SET_PORTFOLIOS(state, portfolios) {
      state.portfolios = portfolios
    },
    SET_CURRENT_PORTFOLIO(state, portfolio) {
      state.currentPortfolio = portfolio
    },
    SET_TRANSACTIONS(state, transactions) {
      state.transactions = transactions
    },
    SET_PERFORMANCE(state, performance) {
      state.performance = performance
    },
    ADD_PORTFOLIO(state, portfolio) {
      state.portfolios.push(portfolio)
    },
    UPDATE_PORTFOLIO(state, updatedPortfolio) {
      const index = state.portfolios.findIndex(p => p.id === updatedPortfolio.id)
      if (index !== -1) {
        state.portfolios.splice(index, 1, updatedPortfolio)
      }
      if (state.currentPortfolio && state.currentPortfolio.id === updatedPortfolio.id) {
        state.currentPortfolio = updatedPortfolio
      }
    },
    REMOVE_PORTFOLIO(state, portfolioId) {
      state.portfolios = state.portfolios.filter(p => p.id !== portfolioId)
      if (state.currentPortfolio && state.currentPortfolio.id === portfolioId) {
        state.currentPortfolio = null
      }
    },
    ADD_TRANSACTION(state, transaction) {
      state.transactions.push(transaction)
    }
  },
  actions: {
    async fetchPortfolios({ commit, dispatch }) {
      try {
        const response = await api.get('/portfolios')
        commit('SET_PORTFOLIOS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des portefeuilles', { root: true })
        throw error
      }
    },
    async fetchPortfolio({ commit, dispatch }, portfolioId) {
      try {
        const response = await api.get(`/portfolios/${portfolioId}`)
        commit('SET_CURRENT_PORTFOLIO', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération du portefeuille', { root: true })
        throw error
      }
    },
    async createPortfolio({ commit, dispatch }, portfolioData) {
      try {
        const response = await api.post('/portfolios', portfolioData)
        commit('ADD_PORTFOLIO', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la création du portefeuille', { root: true })
        throw error
      }
    },
    async updatePortfolio({ commit, dispatch }, { portfolioId, portfolioData }) {
      try {
        const response = await api.put(`/portfolios/${portfolioId}`, portfolioData)
        commit('UPDATE_PORTFOLIO', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la mise à jour du portefeuille', { root: true })
        throw error
      }
    },
    async deletePortfolio({ commit, dispatch }, portfolioId) {
      try {
        await api.delete(`/portfolios/${portfolioId}`)
        commit('REMOVE_PORTFOLIO', portfolioId)
        return { success: true }
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la suppression du portefeuille', { root: true })
        throw error
      }
    },
    async addTransaction({ commit, dispatch }, { portfolioId, transactionData }) {
      try {
        const response = await api.post(`/portfolios/${portfolioId}/transactions`, transactionData)
        commit('ADD_TRANSACTION', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de l\'ajout de la transaction', { root: true })
        throw error
      }
    },
    async fetchPerformance({ commit, dispatch }, portfolioId) {
      try {
        const response = await api.get(`/portfolios/${portfolioId}/performance`)
        commit('SET_PERFORMANCE', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des performances', { root: true })
        throw error
      }
    }
  }
}
