<script setup lang="ts">
const props = defineProps<{
  id: string;
  name: string;
  testId?: string;
  invalid?: boolean;
  placeholder?: string;
}>();
</script>

<template>
  <input
    type="text"
    v-bind="props"
    :data-testid="testId"
    class="input-style"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
    ]"
  />
</template>
