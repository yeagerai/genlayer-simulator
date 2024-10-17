<script setup>
import { QuestionMarkCircleIcon } from '@heroicons/vue/16/solid';

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <QuestionMarkCircleIcon
    class="h-3 w-3 shrink-0 opacity-70 hover:opacity-100"
    v-tooltip="text"
  />
</template>
