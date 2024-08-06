<script setup lang="ts">
const props = defineProps<{
  id: string;
  name: string;
  min?: number;
  step?: number;
  testId?: string;
  invalid?: boolean;
  placeholder?: string;
  tiny?: boolean;
}>();

const model = defineModel();
</script>

<template>
  <input
    type="number"
    v-bind="props"
    v-model="model"
    :data-testid="testId"
    class="input-style"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
      tiny && 'px-2 py-1',
    ]"
  />
</template>
