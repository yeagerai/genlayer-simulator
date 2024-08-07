<script setup lang="ts">
const emit = defineEmits(['click']);
defineProps({
  id: { type: String, default: null },
  disabled: { type: Boolean, default: false },
});
</script>

<template>
  <button
    :id="id"
    class="flex items-center gap-1 justify-center rounded-md bg-opacity-10 p-1 font-semibold text-primary transition-all hover:bg-slate-200 active:scale-90 dark:text-white dark:hover:bg-zinc-600"
    :class="disabled && 'cursor-not-allowed opacity-50'"
    :disabled="disabled"
    @click="emit('click')"
  >
    <slot />
  </button>
</template>
