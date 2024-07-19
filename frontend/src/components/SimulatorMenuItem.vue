<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { computed } from 'vue'

const props = defineProps({
  to: { type: Object, default: null },
  href: { type: String, default: '/' },
  tooltip: { type: String, default: '' },
});

const isExternal = computed(() => !props.to && props.href);
</script>

<template>
  <RouterLink v-if="!isExternal" :to="to" v-slot="{ isActive }">
    <div
      class="w-12 p-3 hover:bg-slate-100 dark:hover:bg-zinc-700 transition-colors border-r-[3px] border-transparent hover:border-r-primary dark:hover:border-r-accent"
      :class="isActive && !isExternal && 'opacity-100 bg-slate-200 dark:bg-zinc-600 border-r-primary dark:border-r-accent'">

      <div class="h-6 w-6 dark:fill-white fill-primary">
        <slot />
      </div>

      <ToolTip :text="tooltip" :options="{ placement: 'right' }" />

    </div>
  </RouterLink>

  <a v-if="isExternal" :href="href" target="_blank">
    <div class="group p-3">
      <div class="h-5 w-5 dark:fill-white fill-primary opacity-80 group-hover:opacity-100">
        <slot />
      </div>

      <ToolTip :text="tooltip" :options="{ placement: 'right' }" />
    </div>
  </a>
</template>
