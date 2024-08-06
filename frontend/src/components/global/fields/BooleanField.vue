<script setup lang="ts">
import CheckboxInput from '../inputs/CheckboxInput.vue';
import { useUniqueId } from '@/hooks';

const fieldId = useUniqueId('checkbox');

const props = defineProps<{
  name: string;
  label?: string;
  testId?: string;
}>();

const model = defineModel();
</script>

<template>
  <div class="flex flex-row items-center gap-2">
    <CheckboxInput v-model="model" v-bind="props" :id="fieldId" />
    <label :for="fieldId">{{ label }}</label>
  </div>
</template>
