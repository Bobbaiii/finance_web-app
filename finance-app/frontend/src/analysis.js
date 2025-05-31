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
    currentAsset: null,
    assetData: null,
    technicalIndicators: null,
    ictConcepts: null,
    searchResults: [],
    favoriteAssets: []
  },
  getters: {
    getCurrentAsset: state => state.currentAsset,
    getAssetData: state => state.assetData,
    getTechnicalIndicators: state => state.technicalIndicators,
    getIctConcepts: state => state.ictConcepts,
    getSearchResults: state => state.searchResults,
    getFavoriteAssets: state => state.favoriteAssets
  },
  mutations: {
    SET_CURRENT_ASSET(state, asset) {
      state.currentAsset = asset
    },
    SET_ASSET_DATA(state, data) {
      state.assetData = data
    },
    SET_TECHNICAL_INDICATORS(state, indicators) {
      state.technicalIndicators = indicators
    },
    SET_ICT_CONCEPTS(state, concepts) {
      state.ictConcepts = concepts
    },
    SET_SEARCH_RESULTS(state, results) {
      state.searchResults = results
    },
    SET_FAVORITE_ASSETS(state, assets) {
      state.favoriteAssets = assets
    }
  },
  actions: {
    async searchAssets({ commit, dispatch }, query) {
      try {
        const response = await api.get('/analysis/search', {
          params: { query }
        })
        commit('SET_SEARCH_RESULTS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la recherche d\'actifs', { root: true })
        throw error
      }
    },
    async getAssetData({ commit, dispatch }, { symbol, period = '1y', interval = '1d' }) {
      try {
        const response = await api.get(`/analysis/asset/${symbol}`, {
          params: { period, interval }
        })
        commit('SET_ASSET_DATA', response.data)
        commit('SET_CURRENT_ASSET', {
          symbol,
          name: response.data.asset_info?.name || symbol,
          type: response.data.asset_info?.instrumentType || 'unknown'
        })
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || `Erreur lors de la récupération des données pour ${symbol}`, { root: true })
        throw error
      }
    },
    async calculateTechnicalIndicators({ commit, dispatch }, { symbol, indicators, period = '1y', interval = '1d' }) {
      try {
        const response = await api.post('/analysis/technical-indicators', null, {
          params: { symbol, indicators: indicators.join(','), period, interval }
        })
        commit('SET_TECHNICAL_INDICATORS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors du calcul des indicateurs techniques', { root: true })
        throw error
      }
    },
    async calculateIctConcepts({ commit, dispatch }, { symbol, concepts, period = '1y', interval = '1d' }) {
      try {
        const response = await api.post('/analysis/ict-analysis', null, {
          params: { symbol, concepts: concepts.join(','), period, interval }
        })
        commit('SET_ICT_CONCEPTS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors du calcul des concepts ICT', { root: true })
        throw error
      }
    },
    async getFavoriteAssets({ commit, dispatch }) {
      try {
        const response = await api.get('/portfolios/favorites')
        commit('SET_FAVORITE_ASSETS', response.data)
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de la récupération des actifs favoris', { root: true })
        throw error
      }
    },
    async addToFavorites({ dispatch }, assetId) {
      try {
        const response = await api.post(`/portfolios/favorites/${assetId}`)
        await dispatch('getFavoriteAssets')
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors de l\'ajout aux favoris', { root: true })
        throw error
      }
    },
    async removeFromFavorites({ dispatch }, assetId) {
      try {
        const response = await api.delete(`/portfolios/favorites/${assetId}`)
        await dispatch('getFavoriteAssets')
        return response.data
      } catch (error) {
        dispatch('setError', error.response?.data?.detail || 'Erreur lors du retrait des favoris', { root: true })
        throw error
      }
    }
  }
}
