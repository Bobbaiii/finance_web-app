<template>
  <div class="page-card space-y-10">
    <page-header
      eyebrow="Vue d'ensemble"
      title="Tableau de bord"
      description="Visualisez en un clin d'œil la santé de vos marchés, portefeuilles et alertes actives."
    />

    <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
      <div class="col-span-1">
        <div class="section-card h-full">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Actifs favoris</h2>
            <router-link
              v-if="favoriteAssets.length === 0"
              to="/analysis/technical"
              class="inline-flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary transition hover:bg-primary/20"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Ajouter
            </router-link>
          </div>
          <div v-if="favoriteAssets.length > 0" class="mt-5 space-y-4">
            <div v-for="asset in favoriteAssets" :key="asset.id" class="stat-card">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-base font-semibold text-neutral-900 dark:text-white">{{ asset.symbol }}</h3>
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ asset.name }}</p>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold" :class="asset.priceChange >= 0 ? 'text-success' : 'text-danger'">
                    {{ formatPrice(asset.last_price) }}
                  </p>
                  <p class="text-sm font-medium" :class="asset.priceChange >= 0 ? 'text-success' : 'text-danger'">
                    {{ formatPercentage(asset.priceChange) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="mt-6 rounded-2xl border border-dashed border-neutral-200/70 py-6 text-center text-neutral-500 dark:border-neutral-700 dark:text-neutral-400">
            <p>Ajoutez vos actifs préférés pour suivre leurs mouvements.</p>
          </div>
        </div>
      </div>

      <div class="col-span-1">
        <div class="section-card h-full">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Indices majeurs</h2>
          <div class="mt-5 space-y-4">
            <div v-for="index in majorIndices" :key="index.symbol" class="stat-card">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-base font-semibold text-neutral-900 dark:text-white">{{ index.symbol }}</h3>
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ index.name }}</p>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold" :class="index.change >= 0 ? 'text-success' : 'text-danger'">
                    {{ formatPrice(index.price) }}
                  </p>
                  <p class="text-sm font-medium" :class="index.change >= 0 ? 'text-success' : 'text-danger'">
                    {{ formatPercentage(index.change) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-span-1">
        <div class="section-card h-full">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Alertes récentes</h2>
          <div v-if="recentAlerts.length > 0" class="mt-5 space-y-4">
            <div v-for="alert in recentAlerts" :key="alert.id" class="stat-card">
              <div class="flex items-start gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-warning/10 text-warning">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-sm font-semibold text-neutral-900 dark:text-white">{{ alert.asset_symbol }}</h3>
                  <p class="text-xs text-neutral-500 dark:text-neutral-400">
                    {{ alert.condition }} {{ formatPrice(alert.value) }}
                  </p>
                  <p class="mt-1 text-xs text-neutral-400 dark:text-neutral-500">
                    {{ formatDate(alert.triggered_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="mt-6 rounded-2xl border border-dashed border-neutral-200/70 py-6 text-center text-neutral-500 dark:border-neutral-700 dark:text-neutral-400">
            <p>Aucune alerte déclenchée récemment.</p>
            <router-link
              to="/alerts/create"
              class="mt-3 inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:bg-primary-dark"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Créer une alerte
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="space-y-6">
      <div>
        <div class="section-card">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Performance du portefeuille</h2>
            <router-link
              v-if="!portfolioPerformance"
              to="/portfolio"
              class="inline-flex items-center gap-2 rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary transition hover:bg-primary/20"
            >
              Configurer
            </router-link>
          </div>
          <div v-if="portfolioPerformance" class="mt-6 grid grid-cols-1 gap-4 md:grid-cols-4">
            <div class="stat-card text-center">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Valeur totale</p>
              <p class="mt-2 text-2xl font-semibold text-neutral-900 dark:text-white">{{ formatPrice(portfolioPerformance.current_value) }}</p>
            </div>
            <div class="stat-card text-center">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Investissement</p>
              <p class="mt-2 text-2xl font-semibold text-neutral-900 dark:text-white">{{ formatPrice(portfolioPerformance.total_invested) }}</p>
            </div>
            <div class="stat-card text-center">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Profit/Perte</p>
              <p class="mt-2 text-2xl font-semibold" :class="portfolioPerformance.profit_loss >= 0 ? 'text-success' : 'text-danger'">
                {{ formatPrice(portfolioPerformance.profit_loss) }}
              </p>
            </div>
            <div class="stat-card text-center">
              <p class="text-sm text-neutral-500 dark:text-neutral-400">Rendement</p>
              <p class="mt-2 text-2xl font-semibold" :class="portfolioPerformance.profit_loss_percentage >= 0 ? 'text-success' : 'text-danger'">
                {{ formatPercentage(portfolioPerformance.profit_loss_percentage) }}
              </p>
            </div>
          </div>
          <div v-else class="mt-6 rounded-2xl border border-dashed border-neutral-200/70 px-6 py-8 text-center text-neutral-500 dark:border-neutral-700 dark:text-neutral-400">
            <p>Créez un portefeuille pour suivre votre performance globale.</p>
            <router-link
              to="/portfolio"
              class="mt-4 inline-flex items-center gap-2 rounded-full bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:bg-primary-dark"
            >
              Créer un portefeuille
            </router-link>
          </div>
        </div>
      </div>

      <div>
        <div class="section-card">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Événements financiers à venir</h2>
          <div v-if="upcomingEvents.length > 0" class="mt-6 overflow-hidden rounded-2xl border border-white/40 dark:border-neutral-700/60">
            <table class="min-w-full divide-y divide-white/40 dark:divide-neutral-700/60">
              <thead class="bg-white/70 backdrop-blur dark:bg-neutral-900/70">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Date</th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Événement</th>
                  <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Impact</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/30 dark:divide-neutral-800/60">
                <tr v-for="event in upcomingEvents" :key="event.id" class="bg-white/60 transition hover:bg-white/90 dark:bg-neutral-900/60 dark:hover:bg-neutral-900/80">
                  <td class="px-6 py-4 text-sm text-neutral-900 dark:text-white">{{ formatDate(event.date) }}</td>
                  <td class="px-6 py-4 text-sm text-neutral-900 dark:text-white">{{ event.title }}</td>
                  <td class="px-6 py-4 text-sm">
                    <span :class="{
                      'badge bg-danger/15 text-danger': event.impact === 'high',
                      'badge bg-warning/15 text-warning': event.impact === 'medium',
                      'badge bg-info/15 text-info': event.impact === 'low'
                    }">
                      {{ event.impact }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="mt-6 rounded-2xl border border-dashed border-neutral-200/70 py-6 text-center text-neutral-500 dark:border-neutral-700 dark:text-neutral-400">
            <p>Aucun événement à venir pour le moment.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/layout/PageHeader.vue'

export default {
  name: 'Dashboard',
  components: {
    PageHeader
  },
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
