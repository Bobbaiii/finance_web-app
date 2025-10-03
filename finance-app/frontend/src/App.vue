<template>
  <div class="app-shell">
    <div class="pointer-events-none absolute inset-0 -z-10">
      <div class="h-full w-full bg-gradient-to-br from-primary/10 via-white/40 to-secondary/10 dark:from-neutral-900/90 dark:via-neutral-950/70 dark:to-neutral-900/80"></div>
      <div class="absolute left-1/2 top-12 h-72 w-72 -translate-x-1/2 rounded-full bg-primary/20 blur-3xl dark:bg-primary/15"></div>
      <div class="absolute bottom-0 right-12 h-64 w-64 rounded-full bg-secondary/20 blur-3xl dark:bg-secondary/15"></div>
    </div>

    <header-component v-if="isAuthenticated" />
    <main class="page-container">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <footer-component v-if="isAuthenticated" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import HeaderComponent from './components/layout/HeaderComponent.vue'
import FooterComponent from './components/layout/FooterComponent.vue'

export default {
  name: 'App',
  components: {
    HeaderComponent,
    FooterComponent
  },
  setup() {
    const store = useStore()
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])

    return {
      isAuthenticated
    }
  }
}
</script>
