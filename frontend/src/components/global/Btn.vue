<script setup lang="ts">
import { computed } from 'vue'
import LoadingIndicator from '@/components/LoadingIndicator.vue'

const emit = defineEmits(['click'])

const props = withDefaults(
  defineProps<{
    id?: string | undefined
    disabled?: boolean
    loading?: boolean
    secondary?: boolean
    dangerous?: boolean
  }>(),
  {
    id: undefined,
    disabled: false,
    loading: false,
    secondary: false,
    dangerous: false,
  },
)

const primary = computed(() => !props.secondary && !props.dangerous)
</script>

<template>
  <button
    :id="id"
    class="flex items-center justify-center gap-2 rounded-md px-4 py-2 font-semibold text-white transition-all hover:text-white active:scale-95"
    :class="[
      primary && 'bg-primary hover:bg-opacity-90 dark:bg-accent',
      secondary &&
        'dark:hover:bg-white-100 border border-gray-300 bg-gray-100 text-gray-700 hover:bg-white hover:text-gray-700 dark:border-none dark:border-gray-400 dark:bg-transparent dark:bg-white dark:bg-opacity-10 dark:text-white dark:shadow-none dark:hover:bg-opacity-20 dark:hover:text-white',
      dangerous && 'bg-red-600 hover:bg-red-500',
      disabled && 'opacity-50 cursor-not-allowed active:scale-100',
    ]"
    :disabled="disabled || loading"
    @click="emit('click')"
  >
    <LoadingIndicator v-if="loading" color="white" />
    <slot />
  </button>
</template>
