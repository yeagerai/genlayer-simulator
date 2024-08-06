<script setup lang="ts">
defineProps<{
  id: string;
  name: string;
  rows?: number;
  cols?: number;
  invalid?: boolean;
}>();

const model = defineModel<string | null>();
</script>

<template>
  <textarea
    :id="id"
    :name="name"
    :rows="rows"
    :cols="cols"
    v-model="model"
    class="input-style"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
    ]"
  />
</template>
