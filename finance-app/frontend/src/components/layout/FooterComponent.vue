<template>
  <div class="bg-neutral-100 dark:bg-neutral-900 py-4">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <p class="text-sm text-neutral-500 dark:text-neutral-400">
          © {{ currentYear }} Finance Analysis Platform. Tous droits réservés.
        </p>
      </div>
    </div>
  </div>
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
