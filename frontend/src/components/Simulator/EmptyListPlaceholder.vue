<template>
  <div class="p-1 text-center text-sm opacity-70">
    <slot v-if="$slots.default" />
    <slot v-else>No items to show.</slot>
  </div>
</template>
