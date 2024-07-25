<script setup lang="ts">
const props = defineProps<{
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
    class="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-accent sm:text-sm sm:leading-6"
    :class="[invalid && 'ring-red-600']"
  />
</template>
