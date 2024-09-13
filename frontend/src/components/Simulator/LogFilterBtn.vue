<script setup lang="ts">
import { Ghost } from 'lucide-vue-next';

// import { useNodeStore } from '@/stores';

// const nodeStore = useNodeStore();
// import { Filter } from 'lucide-vue-next';

defineProps<{
  active: boolean;
}>();
</script>

<template>
  <GhostBtn
    class="border px-1 py-0.5 font-mono text-[10px] font-normal"
    :class="[active && 'border-white', !active && 'border-transparent']"
  >
    <slot />
  </GhostBtn>
</template>
