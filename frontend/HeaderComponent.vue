<template>
  <div class="flex flex-col h-screen">
    <nav class="bg-white dark:bg-neutral-800 shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <router-link to="/dashboard" class="text-xl font-bold text-primary">Finance Analysis</router-link>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/dashboard" 
                class="border-transparent text-neutral-500 dark:text-neutral-300 hover:border-primary hover:text-primary dark:hover:text-primary inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-primary text-primary': isActive('dashboard') }"
              >
                Tableau de bord
              </router-link>
              <router-link 
                to="/analysis/technical" 
                class="border-transparent text-neutral-500 dark:text-neutral-300 hover:border-primary hover:text-primary dark:hover:text-primary inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-primary text-primary': isActive('analysis') }"
              >
                Analyse
              </router-link>
              <router-link 
                to="/portfolio" 
                class="border-transparent text-neutral-500 dark:text-neutral-300 hover:border-primary hover:text-primary dark:hover:text-primary inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-primary text-primary': isActive('portfolio') }"
              >
                Portefeuille
              </router-link>
              <router-link 
                to="/alerts" 
                class="border-transparent text-neutral-500 dark:text-neutral-300 hover:border-primary hover:text-primary dark:hover:text-primary inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-primary text-primary': isActive('alerts') }"
              >
                Alertes
              </router-link>
              <router-link 
                to="/calendar" 
                class="border-transparent text-neutral-500 dark:text-neutral-300 hover:border-primary hover:text-primary dark:hover:text-primary inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="{ 'border-primary text-primary': isActive('calendar') }"
              >
                Calendrier
              </router-link>
            </div>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:items-center">
            <button 
              @click="toggleDarkMode" 
              class="p-1 rounded-full text-neutral-500 dark:text-neutral-300 hover:text-primary dark:hover:text-primary focus:outline-none"
            >
              <span class="sr-only">Changer de thème</span>
              <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>

            <div class="ml-3 relative">
              <div>
                <button 
                  @click="toggleUserMenu" 
                  class="bg-white dark:bg-neutral-800 rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
                >
                  <span class="sr-only">Ouvrir le menu utilisateur</span>
                  <div class="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center">
                    {{ userInitials }}
                  </div>
                </button>
              </div>
              <div 
                v-if="userMenuOpen" 
                class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white dark:bg-neutral-800 ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
              >
                <router-link 
                  to="/settings" 
                  class="block px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700"
                  @click="userMenuOpen = false"
                >
                  Paramètres
                </router-link>
                <a 
                  href="#" 
                  @click.prevent="logout" 
                  class="block px-4 py-2 text-sm text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700"
                >
                  Déconnexion
                </a>
              </div>
            </div>
          </div>
          <div class="-mr-2 flex items-center sm:hidden">
            <button 
              @click="toggleMobileMenu" 
              class="inline-flex items-center justify-center p-2 rounded-md text-neutral-400 hover:text-neutral-500 hover:bg-neutral-100 dark:hover:bg-neutral-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary"
            >
              <span class="sr-only">Ouvrir le menu principal</span>
              <svg 
                :class="{ 'hidden': mobileMenuOpen, 'block': !mobileMenuOpen }" 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg 
                :class="{ 'block': mobileMenuOpen, 'hidden': !mobileMenuOpen }" 
                class="h-6 w-6" 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div :class="{ 'block': mobileMenuOpen, 'hidden': !mobileMenuOpen }" class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            to="/dashboard" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="isActive('dashboard') ? 'border-primary text-primary bg-primary-50 dark:bg-primary-900 dark:bg-opacity-10' : 'border-transparent text-neutral-500 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'"
            @click="mobileMenuOpen = false"
          >
            Tableau de bord
          </router-link>
          <router-link 
            to="/analysis/technical" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="isActive('analysis') ? 'border-primary text-primary bg-primary-50 dark:bg-primary-900 dark:bg-opacity-10' : 'border-transparent text-neutral-500 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'"
            @click="mobileMenuOpen = false"
          >
            Analyse
          </router-link>
          <router-link 
            to="/portfolio" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="isActive('portfolio') ? 'border-primary text-primary bg-primary-50 dark:bg-primary-900 dark:bg-opacity-10' : 'border-transparent text-neutral-500 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'"
            @click="mobileMenuOpen = false"
          >
            Portefeuille
          </router-link>
          <router-link 
            to="/alerts" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="isActive('alerts') ? 'border-primary text-primary bg-primary-50 dark:bg-primary-900 dark:bg-opacity-10' : 'border-transparent text-neutral-500 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'"
            @click="mobileMenuOpen = false"
          >
            Alertes
          </router-link>
          <router-link 
            to="/calendar" 
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="isActive('calendar') ? 'border-primary text-primary bg-primary-50 dark:bg-primary-900 dark:bg-opacity-10' : 'border-transparent text-neutral-500 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'"
            @click="mobileMenuOpen = false"
          >
            Calendrier
          </router-link>
        </div>
        <div class="pt-4 pb-3 border-t border-neutral-200 dark:border-neutral-700">
          <div class="flex items-center px-4">
            <div class="flex-shrink-0">
              <div class="h-10 w-10 rounded-full bg-primary text-white flex items-center justify-center">
                {{ userInitials }}
              </div>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-neutral-800 dark:text-white">{{ user.full_name }}</div>
              <div class="text-sm font-medium text-neutral-500 dark:text-neutral-400">{{ user.email }}</div>
            </div>
            <button 
              @click="toggleDarkMode" 
              class="ml-auto p-1 rounded-full text-neutral-400 hover:text-neutral-500 dark:hover:text-neutral-300 focus:outline-none"
            >
              <span class="sr-only">Changer de thème</span>
              <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </svg>
            </button>
          </div>
          <div class="mt-3 space-y-1">
            <router-link 
              to="/settings" 
              class="block px-4 py-2 text-base font-medium text-neutral-500 dark:text-neutral-300 hover:text-neutral-800 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700"
              @click="mobileMenuOpen = false"
            >
              Paramètres
            </router-link>
            <a 
              href="#" 
              @click.prevent="logout" 
              class="block px-4 py-2 text-base font-medium text-neutral-500 dark:text-neutral-300 hover:text-neutral-800 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-700"
            >
              Déconnexion
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'HeaderComponent',
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    const toast = useToast()

    const mobileMenuOpen = ref(false)
    const userMenuOpen = ref(false)

    const user = computed(() => store.getters['auth/getUser'] || {})
    const isDarkMode = computed(() => store.getters.isDarkMode)

    const userInitials = computed(() => {
      if (!user.value || !user.value.full_name) return '?'
      return user.value.full_name
        .split(' ')
        .map(name => name.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
    })

    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }

    const toggleUserMenu = () => {
      userMenuOpen.value = !userMenuOpen.value
    }

    const toggleDarkMode = () => {
      store.dispatch('toggleDarkMode')
      // Appliquer la classe dark au document
      if (store.getters.isDarkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    const isActive = (routeName) => {
      return route.path.includes(routeName)
    }

    const logout = async () => {
      try {
        await store.dispatch('auth/logout')
        toast.success('Déconnexion réussie')
        router.push('/login')
      } catch (error) {
        toast.error('Erreur lors de la déconnexion')
      }
    }

    // Appliquer le thème au chargement
    if (isDarkMode.value) {
      document.documentElement.classList.add('dark')
    }

    return {
      mobileMenuOpen,
      userMenuOpen,
      user,
      isDarkMode,
      userInitials,
      toggleMobileMenu,
      toggleUserMenu,
      toggleDarkMode,
      isActive,
      logout
    }
  }
}
</script>
