<script setup lang="ts">
const props = defineProps<{
  id: string;
  name: string;
  testId?: string;
  invalid?: boolean;
  placeholder?: string;
  tiny?: boolean;
  forceInteger?: boolean;
}>();

const model = defineModel();

const handleChange = (e: Event) => {
  if (props.forceInteger) {
    const target = e.target as HTMLInputElement;
    model.value = parseInt(target.value, 10);
  }
};

const handleKeydown = (event: KeyboardEvent) => {
  if (
    props.forceInteger &&
    !(event.ctrlKey || event.metaKey) &&
    event.key.length === 1 &&
    isNaN(Number(event.key))
  ) {
    event.preventDefault();
  }
};
</script>

<template>
  <input
    type="number"
    v-bind="props"
    v-model="model"
    lang="en"
    :data-testid="testId"
    class="input-style"
    :class="[
      'hoverinvalid:ring-red-600 invalid:ring-red-600/80',
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
      tiny && 'px-2 py-1',
    ]"
    @input="handleChange"
    @keydown="handleKeydown"
  />
</template>
