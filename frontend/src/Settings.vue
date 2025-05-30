<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">Paramètres</h1>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Profil utilisateur -->
      <div class="col-span-1">
        <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
          <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Profil utilisateur</h2>
          
          <div class="flex items-center mb-6">
            <div class="h-20 w-20 rounded-full bg-primary text-white flex items-center justify-center text-2xl">
              {{ userInitials }}
            </div>
            <div class="ml-4">
              <p class="text-lg font-medium text-neutral-900 dark:text-white">{{ user.full_name }}</p>
              <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ user.email }}</p>
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
      
      <!-- Sécurité -->
      <div class="col-span-1">
        <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
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
      
      <!-- Préférences -->
      <div class="col-span-1">
        <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
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
              Note: Certaines sources peuvent nécessiter une clé API.
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
    
    <!-- Notifications -->
    <div class="mt-6">
      <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
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
                  class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
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
            Enregistrer les paramètres de notification
          </button>
        </div>
      </div>
    </div>
    
    <!-- Exportation de données -->
    <div class="mt-6">
      <div class="bg-neutral-50 dark:bg-neutral-700 p-6 rounded-lg">
        <h2 class="text-lg font-semibold text-neutral-900 dark:text-white mb-4">Exportation de données</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="text-md font-medium text-neutral-900 dark:text-white mb-3">Exporter les données</h3>
            <p class="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
              Exportez vos données pour les sauvegarder ou les utiliser dans d'autres applications.
            </p>
            <div class="space-y-4">
              <button 
                @click="exportPortfolios"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                Exporter les portefeuilles (CSV)
              </button>
              <button 
                @click="exportAlerts"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
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
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-danger hover:bg-danger-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.1
(Content truncated due to size limit. Use line ranges to read in chunks)