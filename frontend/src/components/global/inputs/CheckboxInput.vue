<script setup lang="ts">
const props = defineProps<{
  id: string;
  name: string;
  testId?: string;
  label?: string;
}>();
</script>

<template>
  <input
    v-bind="props"
    :data-testid="testId"
    type="checkbox"
    class="text-primary-600 h-4 w-4 rounded border-gray-300 focus:ring-accent dark:text-accent"
  />
</template>
