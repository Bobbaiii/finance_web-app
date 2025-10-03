<template>
  <div class="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
    <div>
      <p v-if="eyebrow" class="text-xs font-semibold uppercase tracking-[0.4em] text-primary/70 dark:text-primary/60">
        {{ eyebrow }}
      </p>
      <h1 class="text-3xl font-semibold tracking-tight text-neutral-900 dark:text-white sm:text-4xl">
        {{ title }}
      </h1>
      <p v-if="description" class="mt-3 max-w-2xl text-base text-neutral-600 dark:text-neutral-300">
        {{ description }}
      </p>
    </div>
    <div class="flex flex-wrap items-center gap-3">
      <slot name="actions" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: ''
    },
    eyebrow: {
      type: String,
      default: ''
    }
  }
}
</script>
