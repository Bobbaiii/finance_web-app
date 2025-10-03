<template>
  <aside
    class="sidebar"
    :class="[
      isCollapsed ? 'sidebar--collapsed' : '',
      'hidden lg:sticky lg:top-0 lg:flex lg:h-screen lg:flex-col lg:justify-between'
    ]"
  >
    <div>
      <div class="flex items-center justify-between px-5 pt-6">
        <router-link to="/dashboard" class="flex items-center gap-3 text-left">
          <span
            class="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-primary/20 text-primary"
            aria-hidden="true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="h-5 w-5">
              <path
                d="M12 3a9 9 0 00-9 9v5.5A3.5 3.5 0 006.5 21h11a3.5 3.5 0 003.5-3.5V12a9 9 0 00-9-9zm0 2a7 7 0 017 7v5.5c0 .828-.672 1.5-1.5 1.5h-11A1.5 1.5 0 015 17.5V12a7 7 0 017-7zm0 4a3 3 0 00-3 3v2a3 3 0 006 0v-2a3 3 0 00-3-3zm0 2a1 1 0 011 1v2a1 1 0 11-2 0v-2a1 1 0 011-1z"
              />
            </svg>
          </span>
          <div v-if="!isCollapsed" class="flex flex-col">
            <span class="text-base font-semibold text-neutral-900 dark:text-white">Finance Analysis</span>
            <span class="text-xs font-medium text-neutral-500 dark:text-neutral-400">Plateforme d'analyses</span>
          </div>
        </router-link>
        <button
          type="button"
          class="inline-flex h-10 w-10 items-center justify-center rounded-2xl border border-white/50 bg-white/80 text-neutral-500 transition hover:text-primary dark:border-neutral-700/60 dark:bg-neutral-900/70 dark:text-neutral-300"
          @click="toggleSidebar"
        >
          <span class="sr-only">Basculer la navigation</span>
          <svg v-if="isCollapsed" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 6l-6 6 6 6" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6" />
          </svg>
        </button>
      </div>

      <nav class="mt-8 space-y-2 px-3">
        <router-link
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition"
          :class="isActive(item.match)
            ? 'bg-primary text-white shadow-lg'
            : 'text-neutral-600 hover:bg-white/90 hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800/80 dark:hover:text-white'"
        >
          <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-white/70 text-primary shadow-sm transition group-hover:bg-white dark:bg-neutral-900/60 dark:text-primary">
            <navigation-icon :name="item.icon" icon-class="h-5 w-5" />
          </span>
          <div v-if="!isCollapsed" class="flex flex-col">
            <span>{{ item.label }}</span>
            <span class="text-xs font-normal text-neutral-500 opacity-0 transition group-hover:opacity-100 dark:text-neutral-400">
              {{ item.description }}
            </span>
          </div>
        </router-link>
      </nav>
    </div>

    <div class="px-5 pb-8">
      <div
        class="rounded-2xl border border-white/50 bg-white/80 p-4 text-sm shadow-inner backdrop-blur-lg dark:border-neutral-700/60 dark:bg-neutral-900/70"
      >
        <h2 class="text-xs font-semibold uppercase tracking-[0.3em] text-neutral-400 dark:text-neutral-500" v-if="!isCollapsed">
          Conseils rapides
        </h2>
        <p class="mt-1 text-neutral-600 dark:text-neutral-300" v-if="!isCollapsed">
          Personnalisez votre tableau de bord en ajoutant des widgets depuis l'écran d'analyse.
        </p>
        <router-link
          v-if="!isCollapsed"
          to="/settings"
          class="mt-4 inline-flex items-center gap-2 text-xs font-medium text-primary hover:text-primary-dark"
        >
          Gérer mes préférences
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" class="h-4 w-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </router-link>
        <button
          v-else
          @click="toggleSidebar"
          class="mt-1 inline-flex items-center justify-center rounded-lg px-3 py-1 text-xs font-medium text-primary hover:text-primary-dark"
        >
          Ouvrir
        </button>
      </div>
    </div>
  </aside>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavigationIcon from './NavigationIcon.vue'
import { mainNavigation } from '../../constants/navigation'

const STORAGE_KEY = 'sidebar-collapsed'

export default {
  name: 'SidebarNavigation',
  components: {
    NavigationIcon
  },
  setup() {
    const route = useRoute()
    const navigation = mainNavigation
    const isCollapsed = ref(false)

    const initializeState = () => {
      if (typeof window === 'undefined') return
      const stored = localStorage.getItem(STORAGE_KEY)
      isCollapsed.value = stored === 'true'
    }

    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value
      if (typeof window !== 'undefined') {
        localStorage.setItem(STORAGE_KEY, String(isCollapsed.value))
      }
    }

    const isActive = (match) => {
      return route.path.startsWith(match)
    }

    onMounted(() => {
      initializeState()
    })

    return {
      navigation,
      isCollapsed,
      isActive,
      toggleSidebar
    }
  }
}
</script>

<style scoped>
.sidebar {
  @apply relative z-20 bg-white/80 shadow-2xl backdrop-blur-xl transition-all duration-300 ease-in-out dark:bg-neutral-900/80 dark:shadow-none;
  width: 280px;
}

.sidebar--collapsed {
  width: 110px;
}

.sidebar::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 0 32px 32px 0;
  border: 1px solid rgba(255, 255, 255, 0.4);
  pointer-events: none;
}

.dark .sidebar::before {
  border-color: rgba(82, 82, 91, 0.6);
}

.sidebar--collapsed::before {
  border-radius: 0 28px 28px 0;
}
</style>
