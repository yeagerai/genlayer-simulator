<script setup lang="ts">
import { RouterLink } from 'vue-router'

defineProps({
  to: { type: Object, default: null },
  tooltip: { type: String, default: '' },
})
</script>

<template>
  <RouterLink :to="to" v-slot="{ isActive }">
    <div
      class="w-12 border-r-[3px] border-transparent p-3 transition-colors hover:border-r-primary hover:bg-slate-100 dark:hover:border-r-accent dark:hover:bg-zinc-700"
      :class="
        isActive &&
        'border-r-primary bg-slate-200 opacity-100 dark:border-r-accent dark:bg-zinc-600'
      "
    >
      <div class="h-6 w-6 fill-primary dark:fill-white">
        <slot />
      </div>

      <ToolTip :text="tooltip" :options="{ placement: 'right' }" />
    </div>
  </RouterLink>
</template>
