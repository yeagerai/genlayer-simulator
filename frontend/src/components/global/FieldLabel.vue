<script setup lang="ts">
const props = defineProps<{
  for?: string
}>()
</script>

<template>
  <label :for="for" class="block text-sm font-medium leading-8"><slot /></label>
</template>
