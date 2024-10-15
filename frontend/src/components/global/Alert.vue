<script setup lang="ts">
import {
  InformationCircleIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
} from '@heroicons/vue/20/solid';

withDefaults(
  defineProps<{
    info?: boolean;
    success?: boolean;
    warning?: boolean;
    error?: boolean;
  }>(),
  {
    info: false,
    success: false,
    warning: false,
    error: false,
  },
);
</script>

<template>
  <div
    class="rounded-md bg-opacity-20 p-2"
    :class="[
      info && 'bg-blue-500',
      success && 'bg-green-500',
      warning && 'bg-yellow-500',
      error && 'bg-red-500',
    ]"
  >
    <div class="flex">
      <div class="flex-shrink-0">
        <InformationCircleIcon
          v-if="info"
          class="h-5 w-5 text-blue-400"
          aria-hidden="true"
        />
        <CheckCircleIcon
          v-else-if="success"
          class="h-5 w-5 text-green-400"
          aria-hidden="true"
        />
        <ExclamationTriangleIcon
          v-else-if="warning"
          class="h-5 w-5 text-yellow-400"
          aria-hidden="true"
        />
        <XCircleIcon
          v-else-if="error"
          class="h-5 w-5 text-red-400"
          aria-hidden="true"
        />
      </div>

      <div class="ml-3 flex-1 md:flex md:justify-between">
        <p
          class="text-sm"
          :class="[
            info && 'text-gray-600 dark:text-blue-300',
            success && 'text-green-700 dark:text-green-300',
            warning && 'text-yellow-700 dark:text-yellow-300',
            error && 'text-red-700 dark:text-red-300',
          ]"
        >
          <slot></slot>
        </p>
      </div>
    </div>
  </div>
</template>
