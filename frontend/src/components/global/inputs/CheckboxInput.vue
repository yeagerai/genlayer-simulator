<script setup lang="ts">
const props = defineProps<{
  id: string;
  name: string;
  testId?: string;
  label?: string;
}>();

const model = defineModel();
</script>

<template>
  <input
    v-model="model"
    v-bind="props"
    :data-testid="testId"
    type="checkbox"
    class="text-primary-600 h-4 w-4 rounded border-gray-300 text-primary outline-0 focus:ring-accent dark:border-gray-500 dark:bg-transparent dark:text-accent"
  />
</template>
