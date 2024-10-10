<script setup lang="ts">
import NumberInput from '@/components/global/inputs/NumberInput.vue';
import TextInput from '@/components/global/inputs/TextInput.vue';
import SelectInput from '@/components/global/inputs/SelectInput.vue';
import type { NewProviderDataModel } from '@/types';
import { computed } from 'vue';
interface SchemaProperty {
  type?: string | string[];
  default?: any;
  minimum?: number;
  maximum?: number;
  multipleOf?: number;
  enum?: any[];
}

const props = defineProps<{
  name: string;
  property: SchemaProperty;
}>();

const model = defineModel();

const isNumber = computed(
  () => props.property.type === 'number' || props.property.type === 'integer',
);

const isString = computed(() => {
  return (
    props.property.type === 'string' ||
    (props.property.type &&
      props.property.type.length &&
      props.property.type.includes('string') &&
      props.property.type.includes('null'))
  );
});

const isSelect = computed(() => {
  return props.property.enum;
});

const isSupported = computed(() => {
  return isNumber.value || isString.value || isSelect.value;
});
</script>

<template>
  <div
    v-if="isSupported"
    class="flex flex-row items-center justify-between gap-2"
  >
    <div class="font-mono">{{ name }}</div>
    <div class="mr-1 flex flex-row items-center gap-1 text-xs opacity-50">
      <div v-if="property.type">Type: {{ property.type }}</div>
      <div v-if="property.minimum">Min: {{ property.minimum }}</div>
      <div v-if="property.maximum">Max: {{ property.maximum }}</div>
      <div v-if="property.multipleOf">
        Multiple of: {{ property.multipleOf }}
      </div>
    </div>
  </div>

  <NumberInput
    v-if="isNumber"
    v-model="model"
    :id="name"
    :name="name"
    :min="property.minimum"
    :max="property.maximum"
    :step="property.multipleOf"
  />

  <!-- TODO: array -->

  <TextInput v-if="isString" v-model="model" :id="name" :name="name" />

  <SelectInput
    v-if="isSelect"
    v-model="model"
    :id="name"
    :name="name"
    :options="property.enum || []"
  />
</template>

<style lang="css">
/* input:invalid {
  outline: 2px solid red!important;
  border-color: red!important;
  box-shadow: 0 0 0 1px red!important;
} */
</style>
