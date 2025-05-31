<template>
  <div class="min-h-screen bg-neutral-100 dark:bg-neutral-900">
    <header-component v-if="isAuthenticated" />
    <main class="container mx-auto px-4 py-6">
      <router-view />
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
