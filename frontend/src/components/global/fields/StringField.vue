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
  <FieldLabel :for="fieldId">{{ name }}</FieldLabel>
  <TextInput v-model="model" v-bind="props" :id="fieldId" />
</template>
