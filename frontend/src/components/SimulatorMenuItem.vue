<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps({
  to: { type: Object, default: null },
  tooltip: { type: String, default: '' },
});
</script>

<template>
  <RouterLink :to="to" v-slot="{ isActive }">
    <div
      class="w-12 p-3 hover:bg-slate-100 dark:hover:bg-zinc-700 transition-colors border-r-[3px] border-transparent hover:border-r-primary dark:hover:border-r-accent"
      :class="isActive && 'opacity-100 bg-slate-200 dark:bg-zinc-600 border-r-primary dark:border-r-accent'">

      <div class="h-6 w-6 dark:fill-white fill-primary">
        <slot />
      </div>

      <ToolTip :text="tooltip" :options="{ placement: 'right' }" />
    </div>
  </RouterLink>
</template>
