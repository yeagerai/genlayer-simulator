<script setup lang="ts">
defineProps<{
  name: string;
  testId?: string;
  invalid?: boolean;
  options: Array<string | Option | number>;
}>();

interface Option {
  value?: string;
  label?: string;
  disabled?: boolean;
}

const model = defineModel();
</script>

<template>
  <select
    :id="name"
    :name="name"
    :data-testid="testId"
    v-model="model"
    class="block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset transition-colors hover:ring-opacity-100 focus:ring-2 focus:ring-accent sm:text-sm sm:leading-6 dark:bg-zinc-800 dark:text-white"
    :class="[
      invalid && 'ring-red-600/80 hover:ring-red-600',
      !invalid &&
        'ring-gray-400/60 hover:ring-gray-400 dark:ring-zinc-500/60 dark:hover:ring-zinc-500',
    ]"
  >
    <option
      v-for="option in options"
      :key="
        typeof option === 'string' || typeof option === 'number'
          ? option
          : option.value
      "
      :value="
        typeof option === 'string' || typeof option === 'number'
          ? option
          : option.value
      "
      :selected="
        (typeof option === 'string' || typeof option === 'number'
          ? option
          : option.value) === model
      "
      :disabled="
        typeof option === 'string' || typeof option === 'number'
          ? false
          : option.disabled || false
      "
      v-tooltip="'test'"
    >
      {{
        typeof option === 'string' || typeof option === 'number'
          ? option
          : option.label
      }}
      {{
        typeof option === 'string' || typeof option === 'number'
          ? ''
          : option.disabled
            ? '(missing configuration)'
            : ''
      }}
    </option>
  </select>
</template>
