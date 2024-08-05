<template>
  <div
    class="rounded border border-gray-300 p-1 text-center text-sm text-gray-500 dark:border-gray-600 dark:text-gray-400"
  >
    <slot v-if="$slots.default" />
    <slot v-else>No items to show.</slot>
  </div>
</template>
