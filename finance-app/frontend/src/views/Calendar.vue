<template>
  <div class="page-card space-y-10">
    <page-header
      eyebrow="Planification"
      title="Calendrier financier"
      description="Anticipez les publications économiques, résultats et annonces clés pour orchestrer vos décisions d'investissement."
    />

    <div class="section-card space-y-6">
      <div class="flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
        <div class="flex items-center gap-3 rounded-full bg-white/70 px-4 py-2 shadow-inner dark:bg-neutral-900/70">
          <button
            @click="prevMonth"
            class="inline-flex h-9 w-9 items-center justify-center rounded-full text-neutral-600 transition hover:text-primary dark:text-neutral-300 dark:hover:text-primary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <span class="text-sm font-semibold tracking-wide text-neutral-700 dark:text-neutral-200">
            {{ formatMonth(currentMonth) }} {{ currentYear }}
          </span>
          <button
            @click="nextMonth"
            class="inline-flex h-9 w-9 items-center justify-center rounded-full text-neutral-600 transition hover:text-primary dark:text-neutral-300 dark:hover:text-primary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <div class="flex flex-wrap gap-2">
          <button
            v-for="filter in filterOptions"
            :key="filter.value"
            @click="toggleFilter(filter.value)"
            class="rounded-full px-4 py-2 text-xs font-medium uppercase tracking-wide transition"
            :class="activeFilters.includes(filter.value)
              ? 'bg-primary text-white shadow shadow-primary/30'
              : 'bg-white/60 text-neutral-600 hover:bg-white dark:bg-neutral-800/70 dark:text-neutral-300 dark:hover:bg-neutral-800/90'"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>

      <div class="overflow-hidden rounded-2xl border border-white/40 dark:border-neutral-700/60">
        <table class="min-w-full divide-y divide-white/40 dark:divide-neutral-800/60">
          <thead class="bg-white/80 backdrop-blur dark:bg-neutral-900/70">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Date</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Heure</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Événement</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Type</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Impact</th>
              <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-neutral-500 dark:text-neutral-400">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-white/20 dark:divide-neutral-800/60">
            <tr
              v-for="event in filteredEvents"
              :key="event.id"
              class="bg-white/70 transition hover:bg-white/95 dark:bg-neutral-900/70 dark:hover:bg-neutral-900/85"
            >
              <td class="px-6 py-4 text-sm text-neutral-900 dark:text-white">{{ formatDate(event.date) }}</td>
              <td class="px-6 py-4 text-sm text-neutral-600 dark:text-neutral-300">{{ formatTime(event.date) }}</td>
              <td class="px-6 py-4">
                <p class="text-sm font-semibold text-neutral-900 dark:text-white">{{ event.title }}</p>
                <p class="mt-1 text-xs text-neutral-500 dark:text-neutral-400">{{ event.description }}</p>
              </td>
              <td class="px-6 py-4">
                <span :class="eventTypeClass(event.type)">
                  {{ formatEventType(event.type) }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span :class="impactClass(event.impact)">
                  {{ formatImpact(event.impact) }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm font-medium">
                <div class="flex flex-wrap items-center gap-3">
                  <button
                    v-if="event.can_alert"
                    @click="createAlert(event)"
                    class="inline-flex items-center gap-1 rounded-full bg-primary/10 px-3 py-1 text-xs font-semibold text-primary transition hover:bg-primary/20"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                    Alerte
                  </button>
                  <button
                    @click="addToCalendar(event)"
                    class="inline-flex items-center gap-1 rounded-full bg-white/60 px-3 py-1 text-xs font-semibold text-secondary transition hover:bg-white dark:bg-neutral-800/70 dark:text-secondary-light dark:hover:bg-neutral-800"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Agenda
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="filteredEvents.length === 0" class="rounded-2xl border border-dashed border-neutral-200/70 py-12 text-center dark:border-neutral-700">
        <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h3 class="mt-4 text-lg font-semibold text-neutral-900 dark:text-white">Aucun événement</h3>
        <p class="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
          Ajustez vos filtres ou changez de période pour découvrir de nouvelles opportunités.
        </p>
      </div>
    </div>
  </div>
</template>


<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import PageHeader from '@/components/layout/PageHeader.vue'

export default {
  name: 'Calendar',
  components: {
    PageHeader
  },
  setup() {
    const router = useRouter()
    const toast = useToast()

    const events = ref([])
    const currentMonth = ref(new Date().getMonth())
    const currentYear = ref(new Date().getFullYear())
    const activeFilters = ref(['all'])

    const filterOptions = [
      { label: 'Tous', value: 'all' },
      { label: 'Résultats', value: 'earnings' },
      { label: 'Données économiques', value: 'economic' },
      { label: 'Banques centrales', value: 'central_bank' },
      { label: 'IPO', value: 'ipo' },
      { label: 'Dividendes', value: 'dividend' },
      { label: 'Splits', value: 'split' }
    ]

    onMounted(() => {
      events.value = createSampleEvents(currentYear.value, currentMonth.value)
    })

    const filteredEvents = computed(() => {
      const month = currentMonth.value
      const year = currentYear.value

      const byDate = (event) => {
        const eventDate = new Date(event.date)
        return eventDate.getMonth() === month && eventDate.getFullYear() === year
      }

      const base = events.value.filter(byDate)

      if (activeFilters.value.includes('all')) {
        return base.sort((a, b) => new Date(a.date) - new Date(b.date))
      }

      return base
        .filter(event => activeFilters.value.includes(event.type))
        .sort((a, b) => new Date(a.date) - new Date(b.date))
    })

    const prevMonth = () => {
      if (currentMonth.value === 0) {
        currentMonth.value = 11
        currentYear.value -= 1
      } else {
        currentMonth.value -= 1
      }
    }

    const nextMonth = () => {
      if (currentMonth.value === 11) {
        currentMonth.value = 0
        currentYear.value += 1
      } else {
        currentMonth.value += 1
      }
    }

    const toggleFilter = (filter) => {
      if (filter === 'all') {
        activeFilters.value = ['all']
        return
      }

      if (activeFilters.value.includes('all')) {
        activeFilters.value = activeFilters.value.filter(item => item !== 'all')
      }

      if (activeFilters.value.includes(filter)) {
        activeFilters.value = activeFilters.value.filter(item => item !== filter)
        if (activeFilters.value.length === 0) {
          activeFilters.value = ['all']
        }
      } else {
        activeFilters.value.push(filter)
      }
    }

    const eventTypeClass = (type) => {
      const mapping = {
        earnings: 'badge bg-primary/15 text-primary',
        economic: 'badge bg-success/15 text-success',
        central_bank: 'badge bg-secondary/15 text-secondary',
        ipo: 'badge bg-warning/15 text-warning',
        dividend: 'badge bg-info/15 text-info',
        split: 'badge bg-neutral-200 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-300'
      }
      return mapping[type] || 'badge bg-neutral-200 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-300'
    }

    const impactClass = (impact) => {
      const mapping = {
        high: 'badge bg-danger/15 text-danger',
        medium: 'badge bg-warning/15 text-warning',
        low: 'badge bg-info/15 text-info'
      }
      return mapping[impact] || 'badge bg-neutral-200 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-300'
    }

    const createAlert = (event) => {
      if (!event?.can_alert) return

      router.push({
        name: 'CreateAlert',
        query: {
          symbol: event.symbol,
          event_id: event.id,
          event_date: new Date(event.date).toISOString()
        }
      })
    }

    const addToCalendar = (event) => {
      const title = encodeURIComponent(event.title)
      const description = encodeURIComponent(event.description || '')
      const location = encodeURIComponent('Finance App')
      const startDate = new Date(event.date)
      const endDate = new Date(startDate.getTime() + 60 * 60 * 1000)

      const toCalendarDate = (date) => date.toISOString().replace(/-|:|\.\d+/g, '')
      const start = toCalendarDate(startDate)
      const end = toCalendarDate(endDate)

      const googleCalendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${description}&location=${location}&dates=${start}/${end}`
      window.open(googleCalendarUrl, '_blank')
      toast.success('Événement prêt à être ajouté à votre calendrier')
    }

    const formatDate = (date) => new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })

    const formatTime = (date) => new Date(date).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    })

    const formatEventType = (type) => {
      const labels = {
        earnings: 'Résultats',
        economic: 'Données économiques',
        central_bank: 'Banques centrales',
        ipo: 'IPO',
        dividend: 'Dividendes',
        split: 'Splits'
      }
      return labels[type] || type
    }

    const formatImpact = (impact) => {
      const labels = {
        high: 'Élevé',
        medium: 'Moyen',
        low: 'Faible'
      }
      return labels[impact] || impact
    }

    const formatMonth = (month) => {
      const months = [
        'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
        'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
      ]
      return months[month] || ''
    }

    return {
      events,
      currentMonth,
      currentYear,
      activeFilters,
      filterOptions,
      filteredEvents,
      prevMonth,
      nextMonth,
      toggleFilter,
      createAlert,
      addToCalendar,
      eventTypeClass,
      impactClass,
      formatDate,
      formatTime,
      formatEventType,
      formatImpact,
      formatMonth
    }
  }
}

function createSampleEvents(year, month) {
  return [
    {
      id: 1,
      title: 'Publication des résultats Apple Inc.',
      description: 'Résultats du 2ème trimestre fiscal 2025',
      date: new Date(year, month, 5, 16, 30),
      type: 'earnings',
      impact: 'high',
      can_alert: true,
      symbol: 'AAPL'
    },
    {
      id: 2,
      title: 'Décision de taux BCE',
      description: 'Annonce des taux directeurs par la Banque Centrale Européenne',
      date: new Date(year, month, 10, 13, 45),
      type: 'central_bank',
      impact: 'high',
      can_alert: false
    },
    {
      id: 3,
      title: "Indice des prix à la consommation (IPC)",
      description: "Publication mensuelle de l'inflation en zone euro",
      date: new Date(year, month, 15, 11, 0),
      type: 'economic',
      impact: 'medium',
      can_alert: false
    },
    {
      id: 4,
      title: 'Dividende Microsoft',
      description: 'Date de détachement du dividende trimestriel',
      date: new Date(year, month, 18, 9, 30),
      type: 'dividend',
      impact: 'low',
      can_alert: true,
      symbol: 'MSFT'
    },
    {
      id: 5,
      title: 'IPO TechStartup Inc.',
      description: 'Introduction en bourse sur le Nasdaq',
      date: new Date(year, month, 22, 14, 30),
      type: 'ipo',
      impact: 'medium',
      can_alert: true,
      symbol: 'TECH'
    },
    {
      id: 6,
      title: "Split d'actions Amazon",
      description: "Split d'actions 20:1",
      date: new Date(year, month, 25, 9, 30),
      type: 'split',
      impact: 'medium',
      can_alert: true,
      symbol: 'AMZN'
    },
    {
      id: 7,
      title: "Rapport sur l'emploi US",
      description: "Publication mensuelle des chiffres de l'emploi aux États-Unis",
      date: new Date(year, month, 28, 14, 30),
      type: 'economic',
      impact: 'high',
      can_alert: false
    }
  ]
}
</script>
