import { createStore } from 'vuex'
import auth from '../auth'
import portfolio from '../portfolio'
import alerts from '../alerts'
import analysis from '../analysis'

const store = createStore({
  modules: {
    auth,
    portfolio,
    alerts,
    analysis
  },
  state: () => ({
    error: null,
    loading: false
  }),
  getters: {
    getError: state => state.error,
    isLoading: state => state.loading
  },
  mutations: {
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    },
    SET_LOADING(state, isLoading) {
      state.loading = isLoading
    }
  },
  actions: {
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    },
    setLoading({ commit }, isLoading) {
      commit('SET_LOADING', isLoading)
    }
  }
})

export default store
