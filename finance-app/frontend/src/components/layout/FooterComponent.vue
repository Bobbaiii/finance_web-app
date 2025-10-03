<template>
  <footer class="relative z-10 pb-10">
    <div class="mx-auto w-[calc(100%-2rem)] max-w-7xl">
      <div class="glass-panel rounded-3xl px-6 py-5 sm:px-10">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-sm font-medium uppercase tracking-[0.2em] text-neutral-400 dark:text-neutral-500">Finance Analysis</p>
            <p class="mt-1 text-sm text-neutral-600 dark:text-neutral-300">
              Plateforme d'analyse financière moderne et intuitive.
            </p>
          </div>
          <div class="text-sm text-neutral-500 dark:text-neutral-400">
            © {{ currentYear }} Finance Analysis Platform. Tous droits réservés.
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'FooterComponent',
  setup() {
    const currentYear = computed(() => new Date().getFullYear())

    return {
      currentYear
    }
  }
}
</script>
