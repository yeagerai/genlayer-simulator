<script setup lang="ts">
const props = defineProps<{
  for?: string
}>()
</script>

<template>
  <label :for="for" class="mb-1 block text-sm font-medium leading-6"><slot /></label>
</template>
