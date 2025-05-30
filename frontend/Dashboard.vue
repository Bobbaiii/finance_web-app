<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Widgets de suivi -->
      <div class="col-span-1">
        <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Actifs favoris</h2>
        <div v-if="favoriteAssets.length > 0" class="space-y-4">
          <div v-for="asset in favoriteAssets" :key="asset.id" class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-medium text-neutral-900 dark:text-white">{{ asset.symbol }}</h3>
                <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ asset.name }}</p>
              </div>
              <div class="text-right">
                <p class="font-bold" :class="asset.priceChange >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPrice(asset.last_price) }}
                </p>
                <p class="text-sm" :class="asset.priceChange >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPercentage(asset.priceChange) }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-neutral-500 dark:text-neutral-400">Aucun actif favori</p>
          <router-link to="/analysis/technical" class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark">
            Ajouter des favoris
          </router-link>
        </div>
      </div>

      <!-- Widgets d'analyse -->
      <div class="col-span-1">
        <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Indices majeurs</h2>
        <div class="space-y-4">
          <div v-for="index in majorIndices" :key="index.symbol" class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
            <div class="flex justify-between items-center">
              <div>
                <h3 class="font-medium text-neutral-900 dark:text-white">{{ index.symbol }}</h3>
                <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ index.name }}</p>
              </div>
              <div class="text-right">
                <p class="font-bold" :class="index.change >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPrice(index.price) }}
                </p>
                <p class="text-sm" :class="index.change >= 0 ? 'text-success' : 'text-danger'">
                  {{ formatPercentage(index.change) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Widgets d'information -->
      <div class="col-span-1">
        <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Alertes récentes</h2>
        <div v-if="recentAlerts.length > 0" class="space-y-4">
          <div v-for="alert in recentAlerts" :key="alert.id" class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-warning" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-neutral-900 dark:text-white">{{ alert.asset_symbol }}</h3>
                <p class="text-xs text-neutral-500 dark:text-neutral-400">
                  {{ alert.condition }} {{ formatPrice(alert.value) }}
                </p>
                <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
                  {{ formatDate(alert.triggered_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-neutral-500 dark:text-neutral-400">Aucune alerte récente</p>
          <router-link to="/alerts/create" class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark">
            Créer une alerte
          </router-link>
        </div>
      </div>
    </div>

    <!-- Performances du portefeuille -->
    <div class="mt-8">
      <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Performance du portefeuille</h2>
      <div v-if="portfolioPerformance" class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="text-center">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Valeur totale</p>
            <p class="text-2xl font-bold text-neutral-900 dark:text-white">{{ formatPrice(portfolioPerformance.current_value) }}</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Investissement</p>
            <p class="text-2xl font-bold text-neutral-900 dark:text-white">{{ formatPrice(portfolioPerformance.total_invested) }}</p>
          </div>
          <div class="text-center">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Profit/Perte</p>
            <p class="text-2xl font-bold" :class="portfolioPerformance.profit_loss >= 0 ? 'text-success' : 'text-danger'">
              {{ formatPrice(portfolioPerformance.profit_loss) }}
            </p>
          </div>
          <div class="text-center">
            <p class="text-sm text-neutral-500 dark:text-neutral-400">Rendement</p>
            <p class="text-2xl font-bold" :class="portfolioPerformance.profit_loss_percentage >= 0 ? 'text-success' : 'text-danger'">
              {{ formatPercentage(portfolioPerformance.profit_loss_percentage) }}
            </p>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8 bg-neutral-50 dark:bg-neutral-700 rounded-lg">
        <p class="text-neutral-500 dark:text-neutral-400">Aucun portefeuille actif</p>
        <router-link to="/portfolio" class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark">
          Créer un portefeuille
        </router-link>
      </div>
    </div>

    <!-- Calendrier financier -->
    <div class="mt-8">
      <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Événements financiers à venir</h2>
      <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
        <div v-if="upcomingEvents.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-neutral-200 dark:divide-neutral-600">
            <thead>
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Événement</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Impact</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-neutral-200 dark:divide-neutral-600">
              <tr v-for="event in upcomingEvents" :key="event.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-white">{{ formatDate(event.date) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900 dark:text-white">{{ event.title }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="{
                    'px-2 py-1 text-xs font-medium rounded-full': true,
                    'bg-danger-light text-danger': event.impact === 'high',
                    'bg-warning-light text-warning': event.impact === 'medium',
                    'bg-info-light text-info': event.impact === 'low'
                  }">
                    {{ event.impact }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-neutral-500 dark:text-neutral-400">Aucun événement à venir</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const router = useRouter()

    const favoriteAssets = ref([])
    const portfolioPerformance = ref(null)
    const recentAlerts = ref([])
    const upcomingEvents = ref([])

    // Indices majeurs (données statiques pour l'exemple)
    const majorIndices = ref([
      { symbol: '^GSPC', name: 'S&P 500', price: 4500.21, change: 0.75 },
      { symbol: '^DJI', name: 'Dow Jones', price: 35000.45, change: 0.5 },
      { symbol: '^IXIC', name: 'NASDAQ', price: 14800.32, change: -0.25 },
      { symbol: '^FTSE', name: 'FTSE 100', price: 7200.18, change: 0.3 }
    ])

    // Événements financiers à venir (données statiques pour l'exemple)
    upcomingEvents.value = [
      { id: 1, date: new Date(2025, 4, 25), title: 'Rapport sur l\'inflation', impact: 'high' },
      { id: 2, date: new Date(2025, 4, 26), title: 'Décision de taux de la BCE', impact: 'high' },
      { id: 3, date: new Date(2025, 4, 27), title: 'Rapport sur l\'emploi', impact: 'medium' },
      { id: 4, date: new Date(2025, 4, 30), title: 'Résultats trimestriels Apple', impact: 'medium' }
    ]

    onMounted(async () => {
      try {
        // Charger les actifs favoris
        await store.dispatch('analysis/getFavoriteAssets')
        favoriteAssets.value = store.getters['analysis/getFavoriteAssets']

        // Ajouter des données de prix fictives pour l'exemple
        favoriteAssets.value = favoriteAssets.value.map(asset => ({
          ...asset,
          last_price: Math.random() * 1000,
          priceChange: (Math.random() * 10) - 5
        }))

        // Charger les portefeuilles
        await store.dispatch('portfolio/fetchPortfolios')
        const portfolios = store.getters['portfolio/getPortfolios']
        
        // Si des portefeuilles existent, charger les performances du premier
        if (portfolios.length > 0) {
          await store.dispatch('portfolio/fetchPerformance', portfolios[0].id)
          portfolioPerformance.value = store.getters['portfolio/getPerformance']
        }

        // Charger les alertes
        await store.dispatch('alerts/fetchAlerts')
        const alerts = store.getters['alerts/getAlerts']
        
        // Filtrer pour obtenir les alertes récentes (max 3)
        recentAlerts.value = alerts
          .filter(alert => alert.last_triggered)
          .sort((a, b) => new Date(b.last_triggered) - new Date(a.last_triggered))
          .slice(0, 3)
      } catch (error) {
        console.error('Erreur lors du chargement des données du tableau de bord:', error)
      }
    })

    // Fonctions utilitaires pour le formatage
    const formatPrice = (price) => {
      if (!price && price !== 0) return 'N/A'
      return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(price)
    }

    const formatPercentage = (percentage) => {
      if (!percentage && percentage !== 0) return 'N/A'
      const sign = percentage >= 0 ? '+' : ''
      return `${sign}${percentage.toFixed(2)}%`
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('fr-FR', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    }

    return {
      favoriteAssets,
      majorIndices,
      portfolioPerformance,
      recentAlerts,
      upcomingEvents,
      formatPrice,
      formatPercentage,
      formatDate
    }
  }
}
</script>
