<script setup>
import LoadingIndicator from '@/components/LoadingIndicator.vue';

const emit = defineEmits(['click']);
const props = defineProps({
  id: { type: String, default: null },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
});
</script>

<template>
  <button
    :id="id"
    class="flex items-center justify-center gap-2 rounded bg-primary px-4 py-2 font-semibold text-white hover:bg-opacity-90 dark:bg-accent"
    :disabled="disabled || loading"
    @click="emit('click')"
  >
    <LoadingIndicator v-if="loading" color="white" />
    <slot />
  </button>
</template>
