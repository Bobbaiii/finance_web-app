<template>
  <div class="bg-white dark:bg-neutral-800 shadow rounded-lg p-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
      <h1 class="text-2xl font-bold text-neutral-900 dark:text-white">Analyse Technique</h1>
      
      <!-- Barre de recherche -->
      <div class="mt-4 md:mt-0 relative">
        <div class="flex">
          <input
            type="text"
            v-model="searchQuery"
            @input="searchAssets"
            placeholder="Rechercher un actif..."
            class="w-full md:w-64 px-4 py-2 border border-neutral-300 dark:border-neutral-600 rounded-l-md focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-700 dark:text-white"
          />
          <button
            class="bg-primary text-white px-4 py-2 rounded-r-md hover:bg-primary-dark focus:outline-none"
            @click="searchAssets"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
        
        <!-- Résultats de recherche -->
        <div v-if="searchResults.length > 0" class="absolute z-10 mt-1 w-full bg-white dark:bg-neutral-800 shadow-lg rounded-md max-h-60 overflow-y-auto">
          <ul class="py-1">
            <li v-for="result in searchResults" :key="result.symbol" class="px-4 py-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 cursor-pointer" @click="selectAsset(result)">
              <div class="flex justify-between">
                <div>
                  <span class="font-medium text-neutral-900 dark:text-white">{{ result.symbol }}</span>
                  <span class="ml-2 text-sm text-neutral-500 dark:text-neutral-400">{{ result.name }}</span>
                </div>
                <span class="text-xs text-neutral-500 dark:text-neutral-400">{{ result.exchange }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="currentAsset">
      <!-- En-tête de l'actif -->
      <div class="mb-6 flex flex-col md:flex-row md:items-center md:justify-between">
        <div>
          <div class="flex items-center">
            <h2 class="text-xl font-bold text-neutral-900 dark:text-white">{{ currentAsset.symbol }}</h2>
            <span class="ml-2 text-sm text-neutral-500 dark:text-neutral-400">{{ currentAsset.name }}</span>
            <button @click="toggleFavorite" class="ml-2 text-neutral-400 hover:text-yellow-500 focus:outline-none">
              <svg v-if="isFavorite" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </button>
          </div>
          <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ assetInfo.exchange }} · {{ assetInfo.currency }}</p>
        </div>
        <div class="mt-4 md:mt-0 text-right">
          <p class="text-2xl font-bold" :class="priceChange >= 0 ? 'text-success' : 'text-danger'">
            {{ formatPrice(assetInfo.current_price) }}
          </p>
          <p class="text-sm" :class="priceChange >= 0 ? 'text-success' : 'text-danger'">
            {{ formatChange(priceChange, priceChangePercent) }}
          </p>
        </div>
      </div>

      <!-- Onglets d'analyse -->
      <div class="border-b border-neutral-200 dark:border-neutral-700 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button
            @click="activeTab = 'chart'"
            class="py-4 px-1 border-b-2 font-medium text-sm focus:outline-none"
            :class="activeTab === 'chart' ? 'border-primary text-primary' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300'"
          >
            Graphique
          </button>
          <button
            @click="activeTab = 'indicators'"
            class="py-4 px-1 border-b-2 font-medium text-sm focus:outline-none"
            :class="activeTab === 'indicators' ? 'border-primary text-primary' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300'"
          >
            Indicateurs
          </button>
          <button
            @click="activeTab = 'ict'"
            class="py-4 px-1 border-b-2 font-medium text-sm focus:outline-none"
            :class="activeTab === 'ict' ? 'border-primary text-primary' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300'"
          >
            ICT
          </button>
          <button
            @click="activeTab = 'overview'"
            class="py-4 px-1 border-b-2 font-medium text-sm focus:outline-none"
            :class="activeTab === 'overview' ? 'border-primary text-primary' : 'border-transparent text-neutral-500 hover:text-neutral-700 hover:border-neutral-300 dark:text-neutral-400 dark:hover:text-neutral-300'"
          >
            Aperçu
          </button>
        </nav>
      </div>

      <!-- Contenu des onglets -->
      <div>
        <!-- Graphique -->
        <div v-if="activeTab === 'chart'" class="mb-6">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
            <div class="flex space-x-2 mb-4 md:mb-0">
              <button
                v-for="period in periods"
                :key="period.value"
                @click="changePeriod(period.value)"
                class="px-3 py-1 text-sm rounded-md focus:outline-none"
                :class="selectedPeriod === period.value ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
              >
                {{ period.label }}
              </button>
            </div>
            <div class="flex space-x-2">
              <button
                v-for="interval in intervals"
                :key="interval.value"
                @click="changeInterval(interval.value)"
                class="px-3 py-1 text-sm rounded-md focus:outline-none"
                :class="selectedInterval === interval.value ? 'bg-primary text-white' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'"
              >
                {{ interval.label }}
              </button>
            </div>
          </div>
          
          <!-- Conteneur du graphique -->
          <div class="w-full h-96 bg-neutral-50 dark:bg-neutral-700 rounded-lg" ref="chartContainer"></div>
          
          <!-- Légende et contrôles -->
          <div class="mt-4 flex flex-wrap gap-4">
            <div v-for="indicator in activeIndicators" :key="indicator.id" class="flex items-center">
              <div :class="`w-3 h-3 rounded-full mr-2 bg-${indicator.color}`"></div>
              <span class="text-sm text-neutral-700 dark:text-neutral-300">{{ indicator.name }}</span>
              <button @click="removeIndicator(indicator.id)" class="ml-2 text-neutral-400 hover:text-danger focus:outline-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Indicateurs -->
        <div v-if="activeTab === 'indicators'" class="mb-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="indicator in availableIndicators" :key="indicator.id" class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
              <div class="flex justify-between items-center">
                <div>
                  <h3 class="font-medium text-neutral-900 dark:text-white">{{ indicator.name }}</h3>
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ indicator.description }}</p>
                </div>
                <div>
                  <button 
                    @click="toggleIndicator(indicator)"
                    class="px-3 py-1 text-sm rounded-md focus:outline-none"
                    :class="isIndicatorActive(indicator.id) ? 'bg-primary text-white' : 'bg-neutral-200 dark:bg-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-500'"
                  >
                    {{ isIndicatorActive(indicator.id) ? 'Actif' : 'Ajouter' }}
                  </button>
                  <button 
                    @click="showIndicatorInfo(indicator)"
                    class="ml-2 p-1 text-neutral-400 hover:text-primary rounded-full focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- Paramètres de l'indicateur (si actif) -->
              <div v-if="isIndicatorActive(indicator.id)" class="mt-4">
                <div v-for="param in indicator.parameters" :key="param.name" class="mb-2">
                  <label :for="`param-${indicator.id}-${param.name}`" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">
                    {{ param.label }}
                  </label>
                  <input 
                    :id="`param-${indicator.id}-${param.name}`"
                    v-model="param.value"
                    type="number"
                    class="mt-1 block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary dark:bg-neutral-800 dark:text-white text-sm"
                    @change="updateIndicator(indicator)"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ICT -->
        <div v-if="activeTab === 'ict'" class="mb-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="concept in ictConcepts" :key="concept.id" class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
              <div class="flex justify-between items-center">
                <div>
                  <h3 class="font-medium text-neutral-900 dark:text-white">{{ concept.name }}</h3>
                  <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ concept.description }}</p>
                </div>
                <div>
                  <button 
                    @click="toggleIctConcept(concept)"
                    class="px-3 py-1 text-sm rounded-md focus:outline-none"
                    :class="isIctConceptActive(concept.id) ? 'bg-primary text-white' : 'bg-neutral-200 dark:bg-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-300 dark:hover:bg-neutral-500'"
                  >
                    {{ isIctConceptActive(concept.id) ? 'Actif' : 'Ajouter' }}
                  </button>
                  <button 
                    @click="showIctConceptInfo(concept)"
                    class="ml-2 p-1 text-neutral-400 hover:text-primary rounded-full focus:outline-none"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                </div>
              </div>
              
              <!-- Résultats ICT (si actif) -->
              <div v-if="isIctConceptActive(concept.id) && ictResults[concept.id]" class="mt-4">
                <div v-for="(result, index) in ictResults[concept.id].slice(0, 3)" :key="index" class="text-sm text-neutral-700 dark:text-neutral-300 mb-1">
                  <span :class="result.type === 'bullish' ? 'text-success' : 'text-danger'">
                    {{ result.type === 'bullish' ? '▲' : '▼' }}
                  </span>
                  {{ formatDate(result.date) }} - {{ formatPrice(result.level) }}
                </div>
                <button v-if="ictResults[concept.id].length > 3" class="text-xs text-primary hover:text-primary-dark mt-2">
                  Voir plus ({{ ictResults[concept.id].length - 3 }})
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Aperçu -->
        <div v-if="activeTab === 'overview'" class="mb-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Informations générales -->
            <div class="bg-neutral-50 dark:bg-neutral-700 p-4 rounded-lg">
              <h3 class="font-medium text-neutral-900 dark:text-white mb-4">Informations générales</h3>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Nom</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetInfo.name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Symbole</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetInfo.symbol }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Bourse</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetInfo.exchange }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Devise</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetInfo.currency }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Secteur</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetInfo.sector || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-neutral-500 dark:text-neutral-400">Industrie</span>
                  <span class="text-sm text-neutral-900 dark:text-white">{{ assetIn
(Content truncated due to size limit. Use line ranges to read in chunks)