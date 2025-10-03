<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">Gestion de Portefeuille</h1>

      <button
        @click="showCreatePortfolioModal = true"
        class="mt-4 md:mt-0 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Créer un portefeuille
      </button>
    </div>

    <div v-if="portfolios.length > 0" class="mb-8">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-neutral-200 dark:divide-neutral-600">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Nom</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Valeur</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Profit/Perte</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Rendement</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-neutral-200 dark:divide-neutral-600">
            <tr v-for="portfolio in portfolios" :key="portfolio.id" class="hover:bg-neutral-50 dark:hover:bg-neutral-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm font-medium text-neutral-900 dark:text-white">{{ portfolio.name }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-neutral-900 dark:text-white">{{ formatPrice(portfolio.current_value) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm" :class="portfolio.profit_loss >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPrice(portfolio.profit_loss) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm" :class="portfolio.profit_loss_percentage >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPercentage(portfolio.profit_loss_percentage) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <router-link :to="`/portfolio/${portfolio.id}`" class="text-primary hover:text-primary-dark mr-3">Détails</router-link>
                <button @click="editPortfolio(portfolio)" class="text-secondary hover:text-secondary-dark mr-3">Modifier</button>
                <button @click="confirmDeletePortfolio(portfolio)" class="text-danger hover:text-danger-dark">Supprimer</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-neutral-900 dark:text-white">Aucun portefeuille</h3>
      <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">Commencez par créer un portefeuille pour suivre vos investissements.</p>
    </div>

    <div v-if="showCreatePortfolioModal" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-neutral-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showCreatePortfolioModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white dark:bg-neutral-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white dark:bg-neutral-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-primary-light sm:mx-0 sm:h-10 sm:w-10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-neutral-900 dark:text-white" id="modal-title">
                  {{ editMode ? 'Modifier le portefeuille' : 'Créer un nouveau portefeuille' }}
                </h3>
                <div class="mt-4">
                  <form @submit.prevent="savePortfolio">
                    <div class="mb-4">
                      <label for="portfolio-name" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Nom du portefeuille</label>
                      <input
                        type="text"
                        id="portfolio-name"
                        v-model="portfolioForm.name"
                        class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white text-sm"
                        required
                      />
                    </div>
                    <div class="mb-4">
                      <label for="portfolio-description" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Description</label>
                      <textarea
                        id="portfolio-description"
                        v-model="portfolioForm.description"
                        rows="3"
                        class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white text-sm"
                      ></textarea>
                    </div>
                    <div class="mb-4">
                      <label for="portfolio-currency" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Devise principale</label>
                      <select
                        id="portfolio-currency"
                        v-model="portfolioForm.currency"
                        class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white text-sm"
                        required
                      >
                        <option value="EUR">EUR - Euro</option>
                        <option value="USD">USD - Dollar américain</option>
                        <option value="GBP">GBP - Livre sterling</option>
                        <option value="JPY">JPY - Yen japonais</option>
                        <option value="CHF">CHF - Franc suisse</option>
                      </select>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-neutral-50 dark:bg-neutral-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="savePortfolio"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:ml-3 sm:w-auto sm:text-sm"
            >
              {{ editMode ? 'Mettre à jour' : 'Créer' }}
            </button>
            <button
              type="button"
              @click="showCreatePortfolioModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-neutral-300 dark:border-neutral-600 shadow-sm px-4 py-2 bg-white dark:bg-neutral-800 text-base font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showDeleteConfirmModal" class="fixed inset-0 z-10 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-neutral-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showDeleteConfirmModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="inline-block align-bottom bg-white dark:bg-neutral-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white dark:bg-neutral-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-danger-light sm:mx-0 sm:h-10 sm:w-10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-neutral-900 dark:text-white" id="modal-title">
                  Supprimer le portefeuille
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">
                    Êtes-vous sûr de vouloir supprimer le portefeuille "{{ portfolioToDelete?.name }}" ? Cette action est irréversible et toutes les données associées seront perdues.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-neutral-50 dark:bg-neutral-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              @click="deletePortfolio"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-danger text-base font-medium text-white hover:bg-danger-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger sm:ml-3 sm:w-auto sm:text-sm"
            >
              Supprimer
            </button>
            <button
              type="button"
              @click="showDeleteConfirmModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-neutral-300 dark:border-neutral-600 shadow-sm px-4 py-2 bg-white dark:bg-neutral-800 text-base font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Portfolio',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    const toast = useToast()

    const portfolios = ref([])
    const showCreatePortfolioModal = ref(false)
    const showDeleteConfirmModal = ref(false)
    const editMode = ref(false)
    const portfolioToDelete = ref(null)

    const portfolioForm = ref({
      id: null,
      name: '',
      description: '',
      currency: 'EUR'
    })

    onMounted(async () => {
      await fetchPortfolios()

      if (
        route.query.action === 'add_transaction' &&
        route.query.asset_id &&
        route.query.symbol
      ) {
        if (portfolios.value.length === 1) {
          router.push({
            name: 'AddTransaction',
            params: { id: portfolios.value[0].id },
            query: {
              asset_id: route.query.asset_id,
              symbol: route.query.symbol,
              price: route.query.price
            }
          })
        }
      }
    })

    const fetchPortfolios = async () => {
      try {
        store.dispatch('setLoading', true)
        await store.dispatch('portfolio/fetchPortfolios')
        portfolios.value = store.getters['portfolio/getPortfolios']
      } catch (error) {
        console.error('Erreur lors de la récupération des portefeuilles :', error)
        toast.error('Impossible de charger les portefeuilles')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const resetForm = () => {
      portfolioForm.value = {
        id: null,
        name: '',
        description: '',
        currency: 'EUR'
      }
      editMode.value = false
    }

    const editPortfolio = (portfolio) => {
      portfolioForm.value = {
        id: portfolio.id,
        name: portfolio.name,
        description: portfolio.description || '',
        currency: portfolio.currency
      }
      editMode.value = true
      showCreatePortfolioModal.value = true
    }

    const savePortfolio = async () => {
      try {
        store.dispatch('setLoading', true)

        if (editMode.value) {
          await store.dispatch('portfolio/updatePortfolio', {
            portfolioId: portfolioForm.value.id,
            portfolioData: {
              name: portfolioForm.value.name,
              description: portfolioForm.value.description,
              currency: portfolioForm.value.currency
            }
          })
          toast.success('Portefeuille mis à jour avec succès')
        } else {
          await store.dispatch('portfolio/createPortfolio', {
            name: portfolioForm.value.name,
            description: portfolioForm.value.description,
            currency: portfolioForm.value.currency
          })
          toast.success('Portefeuille créé avec succès')
        }

        await fetchPortfolios()
        showCreatePortfolioModal.value = false
        resetForm()
      } catch (error) {
        console.error('Erreur lors de l\'enregistrement du portefeuille :', error)
        toast.error('Impossible d\'enregistrer le portefeuille')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const confirmDeletePortfolio = (portfolio) => {
      portfolioToDelete.value = portfolio
      showDeleteConfirmModal.value = true
    }

    const deletePortfolio = async () => {
      if (!portfolioToDelete.value) return

      try {
        store.dispatch('setLoading', true)
        await store.dispatch('portfolio/deletePortfolio', portfolioToDelete.value.id)
        portfolios.value = portfolios.value.filter(p => p.id !== portfolioToDelete.value.id)
        toast.success('Portefeuille supprimé avec succès')
      } catch (error) {
        console.error('Erreur lors de la suppression du portefeuille :', error)
        toast.error('Impossible de supprimer ce portefeuille')
      } finally {
        showDeleteConfirmModal.value = false
        portfolioToDelete.value = null
        store.dispatch('setLoading', false)
      }
    }

    const formatPrice = (value) => {
      if (value === null || value === undefined) {
        return '-'
      }

      const number = Number(value)
      if (Number.isNaN(number)) {
        return value
      }

      return number.toLocaleString('fr-FR', {
        style: 'currency',
        currency: 'EUR'
      })
    }

    const formatPercentage = (value) => {
      if (value === null || value === undefined) {
        return '-'
      }

      const number = Number(value)
      if (Number.isNaN(number)) {
        return value
      }

      return `${number.toFixed(2)} %`
    }

    return {
      portfolios,
      showCreatePortfolioModal,
      showDeleteConfirmModal,
      editMode,
      portfolioForm,
      portfolioToDelete,
      formatPrice,
      formatPercentage,
      editPortfolio,
      savePortfolio,
      confirmDeletePortfolio,
      deletePortfolio,
      resetForm
    }
  }
}
</script>
