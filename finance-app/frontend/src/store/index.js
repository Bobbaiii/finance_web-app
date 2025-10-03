import { createStore } from 'vuex'

import auth from '../auth'
import alerts from '../alerts'
import analysis from '../analysis'
import portfolio from '../portfolio'

const store = createStore({
  state: () => ({
    loading: false,
    error: null
  }),
  getters: {
    isLoading: state => state.loading,
    getError: state => state.error
  },
  mutations: {
    SET_LOADING(state, value) {
      state.loading = value
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  actions: {
    setLoading({ commit }, value) {
      commit('SET_LOADING', value)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('SET_ERROR', null)
    }
  },
  modules: {
    auth,
    alerts,
    analysis,
    portfolio
  }
})

export default store
