<script setup lang="ts">
defineProps<{
  tiny?: boolean;
}>();
</script>

<template>
  <label
    class="block"
    :class="[
      !tiny && 'text-sm font-medium leading-8',
      tiny && 'text-xs font-semibold leading-6',
    ]"
    ><slot
  /></label>
</template>
