<template>
  <header class="relative z-20">
    <nav class="glass-panel mx-auto mt-6 w-[calc(100%-2rem)] max-w-7xl rounded-3xl px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <div class="flex items-center gap-6">
          <router-link to="/dashboard" class="flex items-center text-xl font-semibold tracking-tight text-neutral-900 transition hover:text-primary dark:text-white">
            <span class="mr-2 inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-primary/15 text-primary">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5">
                <path d="M12 3a9 9 0 00-9 9v5.5A3.5 3.5 0 006.5 21h11a3.5 3.5 0 003.5-3.5V12a9 9 0 00-9-9zm0 2a7 7 0 017 7v5.5c0 .828-.672 1.5-1.5 1.5h-11A1.5 1.5 0 015 17.5V12a7 7 0 017-7zm0 4a3 3 0 00-3 3v2a3 3 0 006 0v-2a3 3 0 00-3-3zm0 2a1 1 0 011 1v2a1 1 0 11-2 0v-2a1 1 0 011-1z" />
              </svg>
            </span>
            Finance Analysis
          </router-link>

          <div class="hidden items-center gap-1 rounded-full bg-white/60 px-1 py-1 text-sm font-medium dark:bg-neutral-800/80 md:flex">
            <router-link
              v-for="item in navigation"
              :key="item.route"
              :to="item.to"
              class="inline-flex items-center rounded-full px-4 py-2 transition"
              :class="isActive(item.route)
                ? 'bg-primary text-white shadow-sm'
                : 'text-neutral-500 hover:text-neutral-900 hover:bg-white dark:text-neutral-300 dark:hover:text-white dark:hover:bg-neutral-700/70'"
            >
              {{ item.label }}
            </router-link>
          </div>
        </div>

        <div class="hidden items-center gap-4 md:flex">
          <button
            @click="toggleDarkMode"
            class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/60 bg-white/80 text-neutral-500 transition hover:text-primary dark:border-neutral-700/70 dark:bg-neutral-800/80 dark:text-neutral-300 dark:hover:text-primary"
          >
            <span class="sr-only">Changer de thème</span>
            <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>

          <div class="relative">
            <button
              @click="toggleUserMenu"
              class="flex items-center gap-3 rounded-full border border-white/60 bg-white/80 py-1 pl-1 pr-4 text-sm font-medium text-neutral-700 shadow-sm transition hover:text-primary dark:border-neutral-700/70 dark:bg-neutral-800/80 dark:text-neutral-200"
            >
              <span class="inline-flex h-9 w-9 items-center justify-center rounded-full bg-primary text-white">
                {{ userInitials }}
              </span>
              <span class="hidden lg:block">{{ user.full_name || 'Utilisateur' }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div
              v-if="userMenuOpen"
              class="glass-panel absolute right-0 mt-3 w-56 overflow-hidden rounded-2xl p-2 text-sm shadow-2xl"
            >
              <div class="px-3 py-2 text-xs uppercase tracking-wide text-neutral-400 dark:text-neutral-500">
                Accès rapide
              </div>
              <router-link
                to="/settings"
                class="flex items-center gap-3 rounded-xl px-3 py-2 text-neutral-600 transition hover:bg-white/70 hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-700/80 dark:hover:text-white"
                @click="userMenuOpen = false"
              >
                <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-primary/15 text-primary">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 11V7a4 4 0 118 0v4m-2 4h-4m0 0v4m0-4h4m-4 0H7" />
                  </svg>
                </span>
                Paramètres
              </router-link>
              <button
                @click.prevent="logout"
                class="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left text-neutral-600 transition hover:bg-danger/10 hover:text-danger dark:text-neutral-300 dark:hover:bg-danger/15 dark:hover:text-danger"
              >
                <span class="inline-flex h-8 w-8 items-center justify-center rounded-xl bg-danger/10 text-danger">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8v8" />
                  </svg>
                </span>
                Déconnexion
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-3 md:hidden">
          <button
            @click="toggleDarkMode"
            class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/60 bg-white/80 text-neutral-500 transition hover:text-primary dark:border-neutral-700/70 dark:bg-neutral-800/80 dark:text-neutral-300 dark:hover:text-primary"
          >
            <span class="sr-only">Changer de thème</span>
            <svg v-if="isDarkMode" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
          </button>
          <button
            @click="toggleMobileMenu"
            class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/60 bg-white/80 text-neutral-500 transition hover:text-primary dark:border-neutral-700/70 dark:bg-neutral-800/80 dark:text-neutral-300 dark:hover:text-primary"
          >
            <span class="sr-only">Ouvrir le menu principal</span>
            <svg
              :class="{ hidden: mobileMenuOpen, block: !mobileMenuOpen }"
              class="h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg
              :class="{ block: mobileMenuOpen, hidden: !mobileMenuOpen }"
              class="h-5 w-5"
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

      <div
        :class="{ 'max-h-[460px] opacity-100': mobileMenuOpen, 'max-h-0 opacity-0': !mobileMenuOpen }"
        class="md:hidden overflow-hidden transition-all duration-300 ease-in-out"
      >
        <div class="mt-4 space-y-2 rounded-2xl bg-white/80 p-3 shadow-inner dark:bg-neutral-900/80">
          <router-link
            v-for="item in navigation"
            :key="item.route"
            :to="item.to"
            class="block rounded-xl px-4 py-3 text-sm font-medium transition"
            :class="isActive(item.route)
              ? 'bg-primary/10 text-primary'
              : 'text-neutral-600 hover:bg-white hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800'"
            @click="mobileMenuOpen = false"
          >
            {{ item.label }}
          </router-link>
          <div class="rounded-2xl bg-white/70 p-4 text-sm dark:bg-neutral-900/70">
            <div class="flex items-center gap-3">
              <div class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-primary text-white">
                {{ userInitials }}
              </div>
              <div class="text-sm">
                <p class="font-semibold text-neutral-900 dark:text-white">{{ user.full_name }}</p>
                <p class="text-neutral-500 dark:text-neutral-400">{{ user.email }}</p>
              </div>
            </div>
            <div class="mt-4 grid gap-2">
              <router-link
                to="/settings"
                class="rounded-xl px-3 py-2 text-neutral-600 transition hover:bg-white hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800"
                @click="mobileMenuOpen = false"
              >
                Paramètres
              </router-link>
              <button
                @click.prevent="logout"
                class="rounded-xl px-3 py-2 text-left text-neutral-600 transition hover:bg-danger/10 hover:text-danger dark:text-neutral-300 dark:hover:bg-danger/15 dark:hover:text-danger"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </header>
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

    const navigation = [
      { label: 'Tableau de bord', route: 'dashboard', to: '/dashboard' },
      { label: 'Analyse', route: 'analysis', to: '/analysis/technical' },
      { label: 'Portefeuille', route: 'portfolio', to: '/portfolio' },
      { label: 'Alertes', route: 'alerts', to: '/alerts' },
      { label: 'Calendrier', route: 'calendar', to: '/calendar' }
    ]

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
      navigation,
      toggleMobileMenu,
      toggleUserMenu,
      toggleDarkMode,
      isActive,
      logout
    }
  }
}
</script>
