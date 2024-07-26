<script setup lang="ts">
import { useUIStore } from '@/stores';
const uiStore = useUIStore();
const props = defineProps<{ color?: string }>();
</script>
<template>
  <div class="flex flex-col items-center">
    <VueSpinnerOval
      size="25"
      :color="
        props.color
          ? props.color
          : uiStore.mode === 'light'
            ? '#1a3851'
            : 'white'
      "
      width="50"
    />
    <slot />
  </div>
</template>
