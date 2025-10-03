<template>
  <nav
    class="pointer-events-auto lg:hidden"
    aria-label="Navigation principale mobile"
  >
    <div class="fixed inset-x-0 bottom-0 z-30 flex justify-center px-4 pb-safe">
      <div class="flex w-full max-w-md items-center justify-between rounded-3xl border border-white/60 bg-white/90 px-4 py-3 text-xs font-medium shadow-2xl backdrop-blur-xl dark:border-neutral-700/70 dark:bg-neutral-900/90">
        <router-link
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="flex flex-1 flex-col items-center gap-1 rounded-2xl px-2 py-2 transition"
          :aria-label="item.label"
          :class="isActive(item.match)
            ? 'text-primary'
            : 'text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white'"
        >
          <span
            class="flex h-10 w-10 items-center justify-center rounded-2xl"
            :class="isActive(item.match)
              ? 'bg-primary/15 text-primary'
              : 'bg-white/60 text-neutral-500 dark:bg-neutral-800/80 dark:text-neutral-300'"
            aria-hidden="true"
          >
            <navigation-icon :name="item.icon" icon-class="h-5 w-5" />
          </span>
          <span class="text-[11px] leading-tight">{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
import { useRoute } from 'vue-router'
import NavigationIcon from './NavigationIcon.vue'
import { mainNavigation } from '../../constants/navigation'

export default {
  name: 'MobileBottomNav',
  components: {
    NavigationIcon
  },
  setup() {
    const route = useRoute()
    const navigation = mainNavigation

    const isActive = (match) => route.path.startsWith(match)

    return {
      navigation,
      isActive
    }
  }
}
</script>

<style scoped>
.pb-safe {
  padding-bottom: calc(1rem + env(safe-area-inset-bottom, 0px));
}
</style>
