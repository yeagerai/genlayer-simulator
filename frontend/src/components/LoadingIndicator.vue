<script setup lang="ts">
import { useUIStore } from '@/stores';
const uiStore = useUIStore();
const props = defineProps<{ color?: string }>();
</script>

// TODO: replace this with new comp in all instances
<template>
  <div class="flex flex-col items-center">
    <VueSpinner
      size="16"
      :color="
        props.color
          ? props.color
          : uiStore.mode === 'light'
            ? '#1a3851'
            : 'white'
      "
    />
    <slot />
  </div>
</template>
