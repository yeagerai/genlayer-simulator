<script setup lang="ts">
import NumberInput from '../inputs/NumberInput.vue';
import FieldLabel from './FieldLabel.vue';
import { useUniqueId } from '@/hooks';

const fieldId = useUniqueId('number');

const props = defineProps<{
  name: string;
  label: string;
  testId?: string;
  placeholder?: string;
}>();

const model = defineModel();
</script>

<template>
  <div class="flex w-full flex-col">
    <FieldLabel :for="fieldId" tiny>{{ name }}</FieldLabel>
    <NumberInput
      v-model="model"
      v-bind="props"
      :id="fieldId"
      :step="0.1"
      tiny
    />
  </div>
</template>
