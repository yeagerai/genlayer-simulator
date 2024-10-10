<script setup lang="ts">
import NumberInput from '@/components/global/inputs/NumberInput.vue';
import TextInput from '@/components/global/inputs/TextInput.vue';
import SelectInput from '@/components/global/inputs/SelectInput.vue';
import { computed } from 'vue';

interface SchemaProperty {
  type?: string | string[];
  default?: any;
  minimum?: number;
  maximum?: number;
  multipleOf?: number;
  enum?: any[];
  $comment?: string;
}

const props = defineProps<{
  name: string;
  property: SchemaProperty;
  error?: string;
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

const tooltip = computed(() => {
  let text = [];
  if (props.property.$comment) {
    text.push(props.property.$comment);
  }
  // if (props.property.type) {
  //   text.push(`Type: ${props.property.type}`);
  // }
  if (props.property.minimum !== undefined) {
    text.push(`Min: ${props.property.minimum}`);
  }
  if (props.property.maximum !== undefined) {
    text.push(`Max: ${props.property.maximum}`);
  }
  if (props.property.multipleOf !== undefined) {
    text.push(`Multiple of: ${props.property.multipleOf}`);
  }
  return text.join(' <br/> ');
});
</script>

<template>
  <div v-if="isSupported" class="my-2 grid grid-cols-3 items-center gap-2">
    <div class="col-span-1">
      <div
        class="flex flex-row items-center gap-2 font-mono text-xs font-medium"
      >
        {{ name }}
      </div>
      <div v-if="error" class="text-xs text-red-500">{{ error }}</div>
    </div>

    <div class="col-span-2">
      <NumberInput
        v-if="isNumber"
        v-model="model"
        :id="name"
        :name="name"
        :min="property.minimum"
        :max="property.maximum"
        :step="property.multipleOf"
        :invalid="!!error"
        v-tooltip.right="{
          content: tooltip,
          html: true,
          triggers: ['focus'],
          hideTriggers: ['focus'],
        }"
      />

      <!-- TODO: array -->

      <TextInput
        v-if="isString"
        v-model="model"
        :id="name"
        :name="name"
        :invalid="!!error"
        v-tooltip.right="{
          content: tooltip,
          html: true,
          triggers: ['focus'],
          hideTriggers: ['focus'],
        }"
      />

      <SelectInput
        v-if="isSelect"
        v-model="model"
        :id="name"
        :name="name"
        :options="property.enum || []"
        :invalid="!!error"
      />
    </div>
  </div>
</template>

<style lang="css">
/* input:invalid {
  outline: 2px solid red!important;
  border-color: red!important;
  box-shadow: 0 0 0 1px red!important;
} */
</style>
