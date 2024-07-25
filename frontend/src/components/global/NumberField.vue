<script setup lang="ts">
const props = defineProps<{
  name: string
  min?: number
  step?: number
  testId?: string
  invalid?: boolean
}>()

const model = defineModel()
</script>

<template>
  <input
    type="number"
    v-model="model"
    :data-testid="testId"
    :name="name"
    :min="min"
    :step="step"
    class="block w-full rounded-md border-0 py-1.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-accent sm:text-sm sm:leading-6"
    :class="[invalid && 'ring-red-600']"
  />
</template>
