<template>
  <header class="relative z-20">
    <div class="glass-panel mx-auto mt-6 w-[calc(100%-2rem)] max-w-7xl rounded-3xl px-4 py-4 sm:px-6 lg:px-8">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div class="flex items-center gap-4">
          <div class="inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-primary/10 text-primary">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 4h7l2 3h9v11a2 2 0 01-2 2H5a2 2 0 01-2-2V4z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.3em] text-neutral-400 dark:text-neutral-500">Vue d'ensemble</p>
            <h2 class="text-xl font-semibold text-neutral-900 dark:text-white">
              Bonjour {{ greetingName }}
            </h2>
            <p class="text-sm text-neutral-500 dark:text-neutral-400">
              Suivez vos marchés, alertes et portefeuilles en temps réel.
            </p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <button
            @click="toggleDarkMode"
            class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-white/60 bg-white/80 text-neutral-500 transition hover:text-primary dark:border-neutral-700/70 dark:bg-neutral-800/80 dark:text-neutral-300 dark:hover:text-primary"
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
              <span class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-primary text-white">
                {{ userInitials }}
              </span>
              <span class="hidden sm:block">{{ user.full_name || 'Utilisateur' }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div
              v-if="userMenuOpen"
              class="glass-panel absolute right-0 mt-3 w-60 overflow-hidden rounded-2xl p-3 text-sm shadow-2xl"
            >
              <div class="flex items-center gap-3 rounded-2xl bg-white/60 p-3 dark:bg-neutral-800/60">
                <div class="inline-flex h-10 w-10 items-center justify-center rounded-full bg-primary/15 text-primary">
                  {{ userInitials }}
                </div>
                <div>
                  <p class="text-sm font-semibold text-neutral-900 dark:text-white">{{ user.full_name }}</p>
                  <p class="text-xs text-neutral-500 dark:text-neutral-400">{{ user.email }}</p>
                </div>
              </div>
              <div class="mt-3 grid gap-2">
                <router-link
                  to="/settings"
                  class="flex items-center gap-3 rounded-xl px-3 py-2 text-neutral-600 transition hover:bg-white/70 hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-700/70 dark:hover:text-white"
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
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useTheme } from '@/composables/useTheme'

export default {
  name: 'HeaderComponent',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()

    const userMenuOpen = ref(false)

    const user = computed(() => store.getters['auth/getUser'] || {})
    const { isDarkMode, toggleTheme, initializeTheme } = useTheme()

    const userInitials = computed(() => {
      if (!user.value || !user.value.full_name) return '?'
      return user.value.full_name
        .split(' ')
        .map(name => name.charAt(0))
        .join('')
        .toUpperCase()
        .substring(0, 2)
    })

    const greetingName = computed(() => {
      if (user.value?.full_name) {
        return user.value.full_name.split(' ')[0]
      }
      if (user.value?.first_name) {
        return user.value.first_name
      }
      return 'investisseur'
    })

    const toggleUserMenu = () => {
      userMenuOpen.value = !userMenuOpen.value
    }

    const toggleDarkMode = () => {
      toggleTheme()
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

    initializeTheme()

    return {
      userMenuOpen,
      user,
      isDarkMode,
      userInitials,
      greetingName,
      toggleUserMenu,
      toggleDarkMode,
      logout
    }
  }
}
</script>
