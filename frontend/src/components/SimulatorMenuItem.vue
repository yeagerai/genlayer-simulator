<script setup lang="ts">
import { RouterLink } from 'vue-router';

defineProps({
  to: { type: Object, default: null },
});
</script>

<template>
  <RouterLink :to="to" v-slot="{ isActive }">
    <div
      class="group w-12 border-r-[3px] border-transparent p-3 transition-colors hover:border-r-primary hover:bg-slate-100 dark:hover:border-r-accent"
      :class="[
        isActive &&
          'border-r-primary bg-slate-200 opacity-100 dark:border-r-accent dark:bg-zinc-600 dark:hover:bg-zinc-600',
        !isActive && 'dark:hover:bg-zinc-700',
      ]"
    >
      <div
        class="h-6 w-6 fill-primary transition-all group-active:scale-90 dark:fill-white"
      >
        <slot />
      </div>
    </div>
  </RouterLink>
</template>
