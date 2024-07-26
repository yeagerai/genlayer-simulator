<script setup lang="ts">
defineProps({
  href: { type: String, default: '/' },
  tooltip: { type: String, default: '' },
});
</script>

<template>
  <a :href="href" target="_blank">
    <div class="group p-3">
      <div class="h-5 w-5 fill-primary opacity-80 group-hover:opacity-100 dark:fill-white">
        <slot />
      </div>

      <ToolTip :text="tooltip" :options="{ placement: 'right' }" />
    </div>
  </a>
</template>
