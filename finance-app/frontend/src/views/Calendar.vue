<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">Calendrier Financier</h1>
      
      <div class="mt-4 md:mt-0 flex space-x-2">
        <button 
          @click="prevMonth"
          class="inline-flex items-center px-3 py-2 border border-neutral-300 dark:border-neutral-600 text-sm font-medium rounded-md text-neutral-700 dark:text-neutral-300 bg-white dark:bg-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <span class="inline-flex items-center px-4 py-2 text-sm font-medium text-neutral-700 dark:text-neutral-300">
          {{ formatMonth(currentMonth) }} {{ currentYear }}
        </span>
        <button 
          @click="nextMonth"
          class="inline-flex items-center px-3 py-2 border border-neutral-300 dark:border-neutral-600 text-sm font-medium rounded-md text-neutral-700 dark:text-neutral-300 bg-white dark:bg-neutral-800 hover:bg-neutral-50 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Filtres -->
    <div class="mb-6">
      <div class="flex flex-wrap gap-2">
        <button 
          @click="toggleFilter('all')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('all') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Tous
        </button>
        <button 
          @click="toggleFilter('earnings')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('earnings') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Résultats
        </button>
        <button 
          @click="toggleFilter('economic')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('economic') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Données économiques
        </button>
        <button 
          @click="toggleFilter('central_bank')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('central_bank') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Banques centrales
        </button>
        <button 
          @click="toggleFilter('ipo')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('ipo') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          IPO
        </button>
        <button 
          @click="toggleFilter('dividend')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('dividend') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Dividendes
        </button>
        <button 
          @click="toggleFilter('split')"
          class="px-3 py-1 text-sm rounded-md focus:outline-none"
          :class="activeFilters.includes('split') ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
        >
          Splits
        </button>
      </div>
    </div>

    <!-- Calendrier -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-neutral-200 dark:divide-neutral-600">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Date</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Heure</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Événement</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Impact</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-neutral-200 dark:divide-neutral-600">
          <tr v-for="event in filteredEvents" :key="event.id" class="hover:bg-neutral-50 dark:hover:bg-neutral-700">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-neutral-900 dark:text-white">{{ formatDate(event.date) }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-neutral-900 dark:text-white">{{ formatTime(event.date) }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-neutral-900 dark:text-white">{{ event.title }}</div>
              <div class="text-xs text-neutral-500 dark:text-neutral-400">{{ event.description }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="{
                'px-2 py-1 text-xs font-medium rounded-full': true,
                'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:bg-opacity-30 dark:text-blue-300': event.type === 'earnings',
                'bg-green-100 text-green-800 dark:bg-green-900 dark:bg-opacity-30 dark:text-green-300': event.type === 'economic',
                'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:bg-opacity-30 dark:text-purple-300': event.type === 'central_bank',
                'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:bg-opacity-30 dark:text-yellow-300': event.type === 'ipo',
                'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:bg-opacity-30 dark:text-indigo-300': event.type === 'dividend',
                'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:bg-opacity-30 dark:text-pink-300': event.type === 'split'
              }">
                {{ formatEventType(event.type) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="{
                'px-2 py-1 text-xs font-medium rounded-full': true,
                'bg-danger-light text-danger': event.impact === 'high',
                'bg-warning-light text-warning': event.impact === 'medium',
                'bg-info-light text-info': event.impact === 'low'
              }">
                {{ formatImpact(event.impact) }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <button 
                @click="createAlert(event)"
                class="text-primary hover:text-primary-dark"
                v-if="event.can_alert"
              >
                Créer une alerte
              </button>
              <button 
                @click="addToCalendar(event)"
                class="text-secondary hover:text-secondary-dark ml-3"
              >
                Ajouter au calendrier
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Message si aucun événement -->
    <div v-if="filteredEvents.length === 0" class="text-center py-12">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-neutral-900 dark:text-white">Aucun événement</h3>
      <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">Aucun événement financier pour cette période avec les filtres sélectionnés.</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Calendar',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()
    
    const events = ref([])
    const currentMonth = ref(new Date().getMonth())
    const currentYear = ref(new Date().getFullYear())
    const activeFilters = ref(['all'])
    
    // Charger les événements (données fictives pour l'exemple)
    onMounted(() => {
      // Simuler le chargement des données depuis l'API
      const now = new Date()
      const startOfMonth = new Date(currentYear.value, currentMonth.value, 1)
      const endOfMonth = new Date(currentYear.value, currentMonth.value + 1, 0)
      
      // Générer des événements fictifs pour le mois en cours
      events.value = [
        {
          id: 1,
          title: 'Publication des résultats Apple Inc.',
          description: 'Résultats du 2ème trimestre fiscal 2025',
          date: new Date(currentYear.value, currentMonth.value, 5, 16, 30),
          type: 'earnings',
          impact: 'high',
          can_alert: true,
          symbol: 'AAPL'
        },
        {
          id: 2,
          title: 'Décision de taux BCE',
          description: 'Annonce des taux directeurs par la Banque Centrale Européenne',
          date: new Date(currentYear.value, currentMonth.value, 10, 13, 45),
          type: 'central_bank',
          impact: 'high',
          can_alert: false
        },
        {
          id: 3,
          title: 'Indice des prix à la consommation (IPC)',
          description: 'Publication mensuelle de l\'inflation en zone euro',
          date: new Date(currentYear.value, currentMonth.value, 15, 11, 0),
          type: 'economic',
          impact: 'medium',
          can_alert: false
        },
        {
          id: 4,
          title: 'Dividende Microsoft',
          description: 'Date de détachement du dividende trimestriel',
          date: new Date(currentYear.value, currentMonth.value, 18, 9, 30),
          type: 'dividend',
          impact: 'low',
          can_alert: true,
          symbol: 'MSFT'
        },
        {
          id: 5,
          title: 'IPO TechStartup Inc.',
          description: 'Introduction en bourse sur le Nasdaq',
          date: new Date(currentYear.value, currentMonth.value, 22, 14, 30),
          type: 'ipo',
          impact: 'medium',
          can_alert: true,
          symbol: 'TECH'
        },
        {
          id: 6,
          title: 'Split d\'actions Amazon',
          description: 'Split d\'actions 20:1',
          date: new Date(currentYear.value, currentMonth.value, 25, 9, 30),
          type: 'split',
          impact: 'medium',
          can_alert: true,
          symbol: 'AMZN'
        },
        {
          id: 7,
          title: 'Rapport sur l\'emploi US',
          description: 'Publication mensuelle des chiffres de l\'emploi aux États-Unis',
          date: new Date(currentYear.value, currentMonth.value, 28, 14, 30),
          type: 'economic',
          impact: 'high',
          can_alert: false
        }
      ]
    })
    
    // Filtrer les événements en fonction des filtres actifs
    const filteredEvents = computed(() => {
      if (activeFilters.value.includes('all')) {
        return events.value.filter(event => {
          const eventDate = new Date(event.date)
          return eventDate.getMonth() === currentMonth.value && eventDate.getFullYear() === currentYear.value
        }).sort((a, b) => new Date(a.date) - new Date(b.date))
      }
      
      return events.value.filter(event => {
        const eventDate = new Date(event.date)
        return eventDate.getMonth() === currentMonth.value && 
               eventDate.getFullYear() === currentYear.value && 
               activeFilters.value.includes(event.type)
      }).sort((a, b) => new Date(a.date) - new Date(b.date))
    })
    
    // Naviguer au mois précédent
    const prevMonth = () => {
      if (currentMonth.value === 0) {
        currentMonth.value = 11
        currentYear.value--
      } else {
        currentMonth.value--
      }
    }
    
    // Naviguer au mois suivant
    const nextMonth = () => {
      if (currentMonth.value === 11) {
        currentMonth.value = 0
        currentYear.value++
      } else {
        currentMonth.value++
      }
    }
    
    // Activer/désactiver un filtre
    const toggleFilter = (filter) => {
      if (filter === 'all') {
        activeFilters.value = ['all']
        return
      }
      
      // Supprimer 'all' si présent
      if (activeFilters.value.includes('all')) {
        activeFilters.value = activeFilters.value.filter(f => f !== 'all')
      }
      
      // Ajouter ou supprimer le filtre
      if (activeFilters.value.includes(filter)) {
        activeFilters.value = activeFilters.value.filter(f => f !== filter)
        
        // Si aucun filtre n'est actif, réactiver 'all'
        if (activeFilters.value.length === 0) {
          activeFilters.value = ['all']
        }
      } else {
        activeFilters.value.push(filter)
      }
    }
    
    // Créer une alerte pour un événement
    const createAlert = (event) => {
      if (!event.can_alert) return
      
      router.push({
        name: 'CreateAlert',
        query: {
          symbol: event.symbol,
          event_id: event.id,
          event_date: event.date.toISOString()
        }
      })
    }
    
    // Ajouter un événement au calendrier personnel
    const addToCalendar = (event) => {
      // Créer un lien pour ajouter l'événement au calendrier
      const title = encodeURIComponent(event.title)
      const description = encodeURIComponent(event.description)
      const location = encodeURIComponent('Finance App')
      const startDate = new Date(event.date)
      const endDate = new Date(startDate.getTime() + 60 * 60 * 1000) // +1 heure
      
      const start = startDate.toISOString().replace(/-|:|\.\d+/g, '')
      const end = endDate.toISOString().replace(/-|:|\.\d+/g, '')
      
      const googleCalendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${description}&location=${location}&dates=${start}/${end}`
      
      // Ouvrir dans un nouvel onglet
      window.open(googleCalendarUrl, '_blank')
      
      toast.success('Événement prêt à être ajouté à votre calendrier')
    }
    
    // Formater la date
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }
    
    // Formater l'heure
    const formatTime = (date
(Content truncated due to size limit. Use line ranges to read in chunks)