<script setup lang="ts">
defineProps<{
  name: string
  testId?: string
  invalid?: boolean
  options: Array<string> | Array<Object> | Object
}>()

const model = defineModel()
</script>

<template>
  <select
    :id="name"
    :name="name"
    :data-testid="testId"
    v-model="model"
    class="block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset transition-colors hover:ring-opacity-100 focus:ring-2 focus:ring-accent sm:text-sm sm:leading-6 dark:bg-zinc-800 dark:text-white"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
    ]"
  >
    <option v-for="option in options" :key="option" :value="option" :selected="option === model">
      {{ option }}
    </option>
  </select>
</template>
