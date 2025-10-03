<template>
  <div class="page-card space-y-10">
    <page-header
      eyebrow="Personnalisation"
      title="Paramètres avancés"
      description="Ajustez votre profil, sécurisez l'accès et adaptez la plateforme à vos préférences."
    />

    <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
      <div class="col-span-1">
        <div class="section-card h-full">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Profil utilisateur</h2>

          <div class="flex items-center mb-6">
            <div class="h-20 w-20 rounded-full bg-primary text-white flex items-center justify-center text-2xl">
              {{ userInitials }}
            </div>
            <div class="ml-4">
              <p class="text-lg font-medium text-neutral-900 dark:text-white">{{ user?.full_name }}</p>
              <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ user?.email }}</p>
            </div>
          </div>

          <form @submit.prevent="updateProfile">
            <div class="mb-4">
              <label for="full-name" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Nom complet</label>
              <input
                type="text"
                id="full-name"
                v-model="profileForm.full_name"
                class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                required
              />
            </div>
            <div class="mb-4">
              <label for="email" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Email</label>
              <input
                type="email"
                id="email"
                v-model="profileForm.email"
                class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                required
              />
            </div>
            <button
              type="submit"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:w-auto sm:text-sm"
            >
              Mettre à jour le profil
            </button>
          </form>
        </div>
      </div>

      <div class="col-span-1">
        <div class="section-card h-full">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Sécurité</h2>

          <form @submit.prevent="updatePassword">
            <div class="mb-4">
              <label for="current-password" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Mot de passe actuel</label>
              <input
                type="password"
                id="current-password"
                v-model="passwordForm.current_password"
                class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                required
              />
            </div>
            <div class="mb-4">
              <label for="new-password" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Nouveau mot de passe</label>
              <input
                type="password"
                id="new-password"
                v-model="passwordForm.new_password"
                class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                required
              />
            </div>
            <div class="mb-4">
              <label for="confirm-password" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Confirmer le mot de passe</label>
              <input
                type="password"
                id="confirm-password"
                v-model="passwordForm.confirm_password"
                class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                required
              />
            </div>
            <button
              type="submit"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:w-auto sm:text-sm"
              :disabled="!isPasswordFormValid"
            >
              Changer le mot de passe
            </button>
          </form>
        </div>
      </div>

      <div class="col-span-1">
        <div class="section-card h-full">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Préférences</h2>

          <div class="mb-6">
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Apparence</h3>
            <div class="flex items-center justify-between">
              <span class="text-sm text-neutral-700 dark:text-neutral-300">Mode sombre</span>
              <button
                @click="toggleDarkMode"
                class="relative inline-flex items-center h-6 rounded-full w-11 focus:outline-none"
                :class="isDarkMode ? 'bg-primary' : 'bg-neutral-300 dark:bg-neutral-600'"
              >
                <span
                  class="inline-block w-4 h-4 transform bg-white rounded-full transition-transform"
                  :class="isDarkMode ? 'translate-x-6' : 'translate-x-1'"
                ></span>
              </button>
            </div>
          </div>

          <div class="mb-6">
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Devise par défaut</h3>
            <select
              v-model="preferences.default_currency"
              class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
            >
              <option value="EUR">EUR - Euro</option>
              <option value="USD">USD - Dollar américain</option>
              <option value="GBP">GBP - Livre sterling</option>
              <option value="JPY">JPY - Yen japonais</option>
              <option value="CHF">CHF - Franc suisse</option>
            </select>
          </div>

          <div class="mb-6">
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Source de données</h3>
            <select
              v-model="preferences.data_source"
              class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
            >
              <option value="yahoo_finance">Yahoo Finance</option>
              <option value="alpha_vantage">Alpha Vantage</option>
              <option value="finnhub">Finnhub</option>
            </select>
            <p class="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
              Note : certaines sources peuvent nécessiter une clé API.
            </p>
          </div>

          <button
            @click="savePreferences"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:w-auto sm:text-sm"
          >
            Enregistrer les préférences
          </button>
        </div>
      </div>
    </div>

    <div class="section-card">
        <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Paramètres de notification</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Canaux de notification</h3>
            <div class="space-y-4">
              <div class="flex items-center">
                <input
                  id="notify-email"
                  type="checkbox"
                  v-model="notificationSettings.email_enabled"
                  class="h-4 w-4 text-primary focus:ring-primary border-neutral-300 dark:border-neutral-700 rounded dark:bg-neutral-800"
                />
                <label for="notify-email" class="ml-2 block text-sm text-neutral-900 dark:text-neutral-300">
                  Email
                </label>
              </div>
              <div class="flex items-center">
                <input
                  id="notify-telegram"
                  type="checkbox"
                  v-model="notificationSettings.telegram_enabled"
                  class="h-4 w-4 text-primary focus:ring-primary border-neutral-300 dark:border-neutral-700 rounded dark:bg-neutral-800"
                />
                <label for="notify-telegram" class="ml-2 block text-sm text-neutral-900 dark:text-neutral-300">
                  Telegram
                </label>
              </div>
              <div class="flex items-center">
                <input
                  id="notify-whatsapp"
                  type="checkbox"
                  v-model="notificationSettings.whatsapp_enabled"
                  class="h-4 w-4 text-primary focus:ring-primary border-neutral-300 dark:border-neutral-700 rounded dark:bg-neutral-800"
                />
                <label for="notify-whatsapp" class="ml-2 block text-sm text-neutral-900 dark:text-neutral-300">
                  WhatsApp
                </label>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Configuration</h3>
            <div class="space-y-4">
              <div v-if="notificationSettings.telegram_enabled">
                <label for="telegram-chat-id" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">ID de chat Telegram</label>
                <input
                  type="text"
                  id="telegram-chat-id"
                  v-model="notificationSettings.telegram_chat_id"
                  class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                  placeholder="Exemple : 123456789"
                />
                <p class="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
                  Pour obtenir votre ID de chat, envoyez un message à @userinfobot sur Telegram.
                </p>
              </div>
              <div v-if="notificationSettings.whatsapp_enabled">
                <label for="whatsapp-number" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Numéro WhatsApp</label>
                <input
                  type="text"
                  id="whatsapp-number"
                  v-model="notificationSettings.whatsapp_number"
                  class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                  placeholder="Exemple : +33612345678"
                />
                <p class="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
                  Entrez votre numéro au format international (avec le code pays).
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 flex justify-end">
          <button
            @click="saveNotificationSettings"
            class="inline-flex items-center gap-2 rounded-full bg-primary px-5 py-2 text-sm font-semibold text-white shadow hover:bg-primary-dark"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Enregistrer les notifications
          </button>
        </div>
      </div>
    </div>

    <div class="section-card space-y-6">
      <h2 class="text-lg font-semibold text-neutral-900 dark:text-white">Exportation de données</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Exporter les données</h3>
            <p class="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
              Exportez vos données pour les sauvegarder ou les utiliser dans d'autres applications.
            </p>
            <div class="space-y-3">
              <button
                @click="exportPortfolios"
                class="inline-flex w-full items-center justify-center gap-2 rounded-full bg-primary px-5 py-2 text-sm font-semibold text-white shadow hover:bg-primary-dark"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Exporter les portefeuilles (CSV)
              </button>
              <button
                @click="exportAlerts"
                class="inline-flex w-full items-center justify-center gap-2 rounded-full bg-primary px-5 py-2 text-sm font-semibold text-white shadow hover:bg-primary-dark"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Exporter les alertes (CSV)
              </button>
            </div>
          </div>
          <div>
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Supprimer le compte</h3>
            <p class="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
              Attention : cette action est irréversible et supprimera toutes vos données.
            </p>
            <button
              @click="showDeleteAccountModal = true"
              class="inline-flex items-center gap-2 rounded-full bg-danger px-5 py-2 text-sm font-semibold text-white shadow hover:bg-danger-dark"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.14 21H7.86a2 2 0 01-1.993-1.858L5 7m5 4v6m4-6v6M9 7h6m-7 0h8l1-2.5A2 2 0 0015.13 3H8.87a2 2 0 00-1.87 1.5L6 7z" />
              </svg>
              Supprimer mon compte
            </button>
          </div>
        </div>
      </div>

    <div v-if="showDeleteAccountModal" class="fixed inset-0 z-10 overflow-y-auto" role="dialog" aria-modal="true">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-neutral-500 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showDeleteAccountModal = false"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="modal-content glass-panel inline-block align-bottom text-left overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-danger-light sm:mx-0 sm:h-10 sm:w-10">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-danger" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 9v2m0 4h.01M5 20h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v11a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-neutral-900 dark:text-white">Supprimer mon compte</h3>
                <div class="mt-2">
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">
                    Cette action est irréversible. Toutes vos données (portefeuilles, transactions, alertes) seront définitivement supprimées.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-white/60 px-4 py-3 backdrop-blur dark:bg-neutral-900/60 sm:flex sm:flex-row-reverse sm:px-6">
            <button
              type="button"
              @click="deleteAccount"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-danger text-base font-medium text-white hover:bg-danger-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger sm:ml-3 sm:w-auto sm:text-sm"
            >
              Confirmer la suppression
            </button>
            <button
              type="button"
              @click="showDeleteAccountModal = false"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-neutral-300 dark:border-neutral-600 shadow-sm px-4 py-2 bg-white dark:bg-neutral-800 text-base font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import PageHeader from '@/components/layout/PageHeader.vue'
import { useTheme } from '@/composables/useTheme'

const PREFERENCES_KEY = 'finance-app-preferences'

export default {
  name: 'Settings',
  components: {
    PageHeader
  },
  setup() {
    const store = useStore()
    const toast = useToast()

    const profileForm = ref({
      full_name: '',
      email: ''
    })

    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    })

    const preferences = ref({
      default_currency: 'EUR',
      data_source: 'yahoo_finance'
    })

    const notificationSettings = ref({
      email_enabled: true,
      telegram_enabled: false,
      whatsapp_enabled: false,
      telegram_chat_id: '',
      whatsapp_number: ''
    })

    const { isDarkMode, toggleTheme, initializeTheme } = useTheme()
    const showDeleteAccountModal = ref(false)

    const user = computed(() => store.getters['auth/getUser'])
    const userInitials = computed(() => {
      if (!user.value?.full_name) return '?'
      const parts = user.value.full_name.split(' ')
      return parts.slice(0, 2).map(part => part.charAt(0).toUpperCase()).join('')
    })

    const isPasswordFormValid = computed(() => {
      return (
        passwordForm.value.new_password.length > 0 &&
        passwordForm.value.new_password === passwordForm.value.confirm_password
      )
    })

    onMounted(async () => {
      await loadUserProfile()
      loadPreferences()
      await loadNotificationSettings()
      initializeTheme()
    })

    const loadUserProfile = async () => {
      try {
        if (!user.value) {
          await store.dispatch('auth/fetchUserProfile')
        }
        if (user.value) {
          profileForm.value = {
            full_name: user.value.full_name,
            email: user.value.email
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement du profil :', error)
        toast.error('Impossible de récupérer le profil utilisateur')
      }
    }

    const loadPreferences = () => {
      try {
        const stored = localStorage.getItem(PREFERENCES_KEY)
        if (stored) {
          preferences.value = JSON.parse(stored)
        }
      } catch (error) {
        console.warn('Impossible de charger les préférences sauvegardées :', error)
      }
    }

    const loadNotificationSettings = async () => {
      try {
        const settings = await store.dispatch('auth/getNotificationSettings')
        if (settings) {
          notificationSettings.value = {
            ...notificationSettings.value,
            ...settings
          }
        }
      } catch (error) {
        console.error('Erreur lors du chargement des paramètres de notification :', error)
        toast.error('Impossible de charger les paramètres de notification')
      }
    }

    const updateProfile = async () => {
      try {
        store.dispatch('setLoading', true)
        const updatedUser = {
          ...(user.value || {}),
          full_name: profileForm.value.full_name,
          email: profileForm.value.email
        }
        store.commit('auth/SET_USER', updatedUser)
        toast.success('Profil mis à jour')
      } catch (error) {
        console.error('Erreur lors de la mise à jour du profil :', error)
        toast.error('Impossible de mettre à jour le profil')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const updatePassword = async () => {
      if (!isPasswordFormValid.value) {
        toast.error('Les mots de passe ne correspondent pas')
        return
      }

      try {
        store.dispatch('setLoading', true)
        await new Promise(resolve => setTimeout(resolve, 400))
        toast.success('Mot de passe mis à jour')
        passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
      } catch (error) {
        console.error('Erreur lors de la mise à jour du mot de passe :', error)
        toast.error('Impossible de mettre à jour le mot de passe')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const toggleDarkMode = () => {
      toggleTheme()
    }

    const savePreferences = () => {
      localStorage.setItem(PREFERENCES_KEY, JSON.stringify(preferences.value))
      toast.success('Préférences enregistrées')
    }

    const saveNotificationSettings = async () => {
      try {
        store.dispatch('setLoading', true)
        await store.dispatch('auth/updateNotificationSettings', {
          email_enabled: notificationSettings.value.email_enabled,
          telegram_enabled: notificationSettings.value.telegram_enabled,
          whatsapp_enabled: notificationSettings.value.whatsapp_enabled,
          telegram_chat_id: notificationSettings.value.telegram_chat_id,
          whatsapp_number: notificationSettings.value.whatsapp_number
        })
        toast.success('Paramètres de notification mis à jour')
      } catch (error) {
        console.error('Erreur lors de la mise à jour des paramètres de notification :', error)
        toast.error('Impossible d\'enregistrer les paramètres de notification')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const exportPortfolios = async () => {
      try {
        store.dispatch('setLoading', true)
        if (!store.getters['portfolio/getPortfolios']?.length) {
          await store.dispatch('portfolio/fetchPortfolios')
        }
        const rows = store.getters['portfolio/getPortfolios']
        if (!rows.length) {
          toast.info('Aucun portefeuille à exporter')
          return
        }
        downloadCsv('portefeuilles.csv', rows)
        toast.success('Portefeuilles exportés')
      } catch (error) {
        console.error('Erreur lors de l\'export des portefeuilles :', error)
        toast.error('Impossible d\'exporter les portefeuilles')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const exportAlerts = async () => {
      try {
        store.dispatch('setLoading', true)
        if (!store.getters['alerts/getAlerts']?.length) {
          await store.dispatch('alerts/fetchAlerts')
        }
        const rows = store.getters['alerts/getAlerts'] || []
        if (!rows.length) {
          toast.info('Aucune alerte à exporter')
          return
        }
        downloadCsv('alertes.csv', rows)
        toast.success('Alertes exportées')
      } catch (error) {
        console.error('Erreur lors de l\'export des alertes :', error)
        toast.error('Impossible d\'exporter les alertes')
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    const deleteAccount = async () => {
      try {
        store.dispatch('setLoading', true)
        await new Promise(resolve => setTimeout(resolve, 400))
        store.commit('auth/CLEAR_AUTH')
        toast.success('Compte supprimé')
      } catch (error) {
        console.error('Erreur lors de la suppression du compte :', error)
        toast.error('Impossible de supprimer le compte')
      } finally {
        showDeleteAccountModal.value = false
        store.dispatch('setLoading', false)
      }
    }

    const downloadCsv = (filename, rows) => {
      const headers = Object.keys(rows[0])
      const csvContent = [
        headers.join(';'),
        ...rows.map(row => headers.map(field => formatCsvValue(row[field])).join(';'))
      ].join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(link.href)
    }

    const formatCsvValue = (value) => {
      if (value === null || value === undefined) {
        return ''
      }
      if (typeof value === 'object') {
        return JSON.stringify(value)
      }
      return String(value).replace(/;/g, ',')
    }

    return {
      profileForm,
      passwordForm,
      preferences,
      notificationSettings,
      isDarkMode,
      showDeleteAccountModal,
      user,
      userInitials,
      isPasswordFormValid,
      updateProfile,
      updatePassword,
      toggleDarkMode,
      savePreferences,
      saveNotificationSettings,
      exportPortfolios,
      exportAlerts,
      deleteAccount
    }
  }
}
</script>
