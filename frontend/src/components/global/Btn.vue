<script setup lang="ts">
import { computed } from 'vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';

const emit = defineEmits(['click']);

const props = withDefaults(
  defineProps<{
    testId?: string | undefined;
    disabled?: boolean;
    loading?: boolean;
    secondary?: boolean;
    dangerous?: boolean;
  }>(),
  {
    testId: undefined,
    disabled: false,
    loading: false,
    secondary: false,
    dangerous: false,
  },
);

const primary = computed(() => !props.secondary && !props.dangerous);
</script>

<template>
  <button
    class="flex items-center justify-center gap-2 rounded-md px-4 py-2 font-semibold transition-all active:scale-95"
    :class="[
      primary && 'bg-primary text-white hover:bg-opacity-90 hover:text-white dark:bg-accent',
      secondary &&
        'dark:hover:bg-white-100 border border-gray-300 bg-gray-100 text-gray-800 hover:bg-white hover:text-gray-800 dark:border-none dark:border-gray-400 dark:bg-transparent dark:bg-white dark:bg-opacity-10 dark:text-white dark:shadow-none dark:hover:bg-opacity-20 dark:hover:text-white',
      dangerous && 'bg-red-600 text-white hover:bg-red-500 hover:text-white',
      disabled && 'cursor-not-allowed opacity-50 active:scale-100',
    ]"
    :disabled="disabled || loading"
    @click="emit('click')"
    :data-testid="testId"
  >
    <LoadingIndicator v-if="loading" color="white" />
    <slot />
  </button>
</template>
