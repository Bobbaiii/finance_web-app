<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">Alertes</h1>
      
      <router-link 
        to="/alerts/create"
        class="mt-4 md:mt-0 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        Créer une alerte
      </router-link>
    </div>

    <!-- Liste des alertes -->
    <div v-if="alerts.length > 0" class="mb-8">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-neutral-200 dark:divide-neutral-600">
          <thead>
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Actif</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Condition</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Valeur</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Statut</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Notifications</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-neutral-200 dark:divide-neutral-600">
            <tr v-for="alert in alerts" :key="alert.id" class="hover:bg-neutral-50 dark:hover:bg-neutral-700">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="text-sm font-medium text-neutral-900 dark:text-white">{{ alert.asset_symbol }}</div>
                  <div class="text-sm text-neutral-500 dark:text-neutral-400 ml-2">{{ alert.asset_name }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-neutral-900 dark:text-white">{{ formatCondition(alert.condition_type) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-neutral-900 dark:text-white">{{ formatPrice(alert.target_value) }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="{
                  'px-2 py-1 text-xs font-medium rounded-full': true,
                  'bg-success-light text-success': alert.is_active && !alert.last_triggered,
                  'bg-warning-light text-warning': alert.is_active && alert.last_triggered,
                  'bg-neutral-200 dark:bg-neutral-600 text-neutral-700 dark:text-neutral-300': !alert.is_active
                }">
                  {{ getAlertStatus(alert) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex space-x-2">
                  <span v-if="alert.notify_email" class="text-neutral-500 dark:text-neutral-400" title="Email">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </span>
                  <span v-if="alert.notify_telegram" class="text-neutral-500 dark:text-neutral-400" title="Telegram">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.97 9.269c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.14.18-.357.295-.6.295-.002 0-.003 0-.005 0l.213-3.054 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.654-.64.135-.954l11.566-4.458c.538-.196 1.006.128.832.952z"/>
                    </svg>
                  </span>
                  <span v-if="alert.notify_whatsapp" class="text-neutral-500 dark:text-neutral-400" title="WhatsApp">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.274.072.376-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564c.173.087.289.13.332.202.043.72.043.433-.101.824z"/>
                      <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm.029 18.88c-1.161 0-2.305-.292-3.318-.844l-3.677.964.984-3.595c-.607-1.052-.927-2.246-.926-3.468.001-3.825 3.113-6.937 6.937-6.937 1.856.001 3.598.723 4.907 2.034 1.31 1.311 2.031 3.054 2.03 4.908-.001 3.825-3.113 6.938-6.937 6.938z"/>
                    </svg>
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="editAlert(alert)" class="text-secondary hover:text-secondary-dark mr-3">Modifier</button>
                <button @click="confirmDeleteAlert(alert)" class="text-danger hover:text-danger-dark">Supprimer</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Message si aucune alerte -->
    <div v-else class="text-center py-12">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-neutral-900 dark:text-white">Aucune alerte</h3>
      <p class="mt-1 text-sm text-neutral-500 dark:text-neutral-400">Commencez par créer une alerte pour être notifié des mouvements de prix.</p>
    </div>

    <!-- Paramètres de notification -->
    <div class="mt-8">
      <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Paramètres de notification</h2>
      <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
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
                  class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white text-sm"
                  placeholder="Exemple: 123456789"
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
                  class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white text-sm"
                  placeholder="Exemple: +33612345678"
                />
                <p class="mt-1 text-xs text-neutral-500 dark:text-neutral-400">
                  Entrez votre numéro au format international (avec le code pays).
                </p>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-6">
          <button 
            @click="saveNotificationSettings"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Enregistrer les paramètres
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmation de suppression -->
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
                  Supprimer l'alerte
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">
                    Êtes-vous sûr de vouloir supprimer l'alerte pour "{{ alertToDelete?.asset_symbol }}" ? Cette action est irréversible.
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-neutral-50 dark:bg-neutral-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button 
              type="button" 
              @click="deleteAlert"
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
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Alerts',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()
    
    const alerts = ref([])
    const showDeleteConfirmModal = ref(false)
    const alertToDelete = ref(null)
    
    const notificationSettings = ref({
      email_enabled: true,
      telegram_enabled: false,
      whatsapp_enabled: false,
      telegram_chat_id: '',
      whatsapp_number: ''
    })
    
    onMounted(async () => {
      await fetchAlerts()
      await fetchNotificationSettings()
    })
    
    const fetchAlerts = async () => {
      try {
        store.dispatch('setLoading', true)
        await store.dispatch('alerts/fetchAlerts')
        alerts.valu
(Content truncated due to size limit. Use line ranges to read in chunks)