<script setup lang="ts">
import TextInput from '../inputs/TextInput.vue';
import FieldLabel from './FieldLabel.vue';
import { useUniqueId } from '@/hooks';

const fieldId = useUniqueId('text');

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
    <TextInput v-model="model" v-bind="props" :id="fieldId" tiny />
  </div>
</template>
