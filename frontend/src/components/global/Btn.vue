<script setup lang="ts">
import { computed } from 'vue';

const emit = defineEmits(['click']);

const props = withDefaults(
  defineProps<{
    testId?: string | undefined;
    disabled?: boolean;
    loading?: boolean;
    secondary?: boolean;
    dangerous?: boolean;
    tiny?: boolean;
  }>(),
  {
    testId: undefined,
    disabled: false,
    loading: false,
    secondary: false,
    dangerous: false,
    tiny: false,
  },
);

const primary = computed(() => !props.secondary && !props.dangerous);
</script>

<template>
  <button
    class="flex items-center justify-center gap-2 font-semibold transition-all active:scale-95"
    :class="[
      primary &&
        'bg-primary text-white hover:bg-opacity-90 hover:text-white dark:bg-accent',
      secondary &&
        'dark:hover:bg-white-100 border border-gray-300 bg-gray-100 text-gray-800 hover:bg-white hover:text-gray-800 dark:border-none dark:border-gray-400 dark:bg-transparent dark:bg-white dark:bg-opacity-10 dark:text-white dark:shadow-none dark:hover:bg-opacity-20 dark:hover:text-white',
      dangerous && 'bg-red-600 text-white hover:bg-red-500 hover:text-white',
      disabled && 'cursor-not-allowed opacity-50 active:scale-100',
      tiny && 'rounded px-2 py-1 text-xs',
      !tiny && 'rounded-md px-4 py-2',
    ]"
    :disabled="disabled || loading"
    @click="emit('click')"
    :data-testid="testId"
  >
    <Loader v-if="loading" forceLightColor />
    <slot />
  </button>
</template>
