<script setup lang="ts">
defineProps({
  href: { type: String, default: '/' },
});
</script>

<template>
  <a :href="href" target="_blank">
    <div class="group p-3">
      <div
        class="h-4 w-4 fill-primary opacity-50 group-hover:opacity-70 dark:fill-white"
      >
        <slot />
      </div>
    </div>
  </a>
</template>
