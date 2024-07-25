<script setup lang="ts">
const props = defineProps<{
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
    class="block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-accent sm:text-sm sm:leading-6"
    :class="[invalid && 'ring-red-600']"
  >
    <option v-for="option in options" :key="option" :value="option" :selected="option === model">
      {{ option }}
    </option>
  </select>
</template>
