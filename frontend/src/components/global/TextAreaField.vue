<script setup lang="ts">
defineProps<{
  name: string
  rows?: number
  cols?: number
  invalid?: boolean
}>()

const model = defineModel<string | null>()
</script>

<template>
  <textarea
    :name="name"
    :rows="rows"
    :cols="cols"
    v-model="model"
    class="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 ring-opacity-90 placeholder:text-gray-400 hover:ring-opacity-100 focus:ring-2 focus:ring-inset focus:ring-accent sm:text-sm sm:leading-6 dark:bg-zinc-800 dark:text-white"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
    ]"
  />
</template>
