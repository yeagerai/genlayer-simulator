<script setup lang="ts">
import providerSchema from '../../../../backend/node/create_nodes/providers_schema.json';
// import { JsonForms } from '@jsonforms/vue';
// import { createAjv } from '@jsonforms/core';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import { computed, defineComponent, markRaw, reactive, ref } from 'vue';
import Ajv2020 from 'ajv/dist/2020';
// import addFormats from 'ajv-formats';
import { type ProviderModel, type NewProviderDataModel } from '@/types';
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
import TextInput from '@/components/global/inputs/TextInput.vue';
import SelectInput from '@/components/global/inputs/SelectInput.vue';
import NumberInput from '@/components/global/inputs/NumberInput.vue';
import TextAreaInput from '@/components/global/inputs/TextAreaInput.vue';
import FieldError from '@/components/global/fields/FieldError.vue';
import FieldLabel from '@/components/global/fields/FieldLabel.vue';

const ajv = new Ajv2020({
  allErrors: true,
  verbose: true,
  strict: true,
  // ...options,
});

const newProviderData = reactive<NewProviderDataModel>({
  model: '',
  provider: '',
  config: {},
  plugin: '',
  plugin_config: {},
});

const schema = markRaw(providerSchema);
console.log(schema);

const validate = ajv.compile(schema);
const errors = ref<any[]>([]);

// const preparedData = computed(() => {
//   const parsedConfig = JSON.parse(newProviderData.config);
//   const parsedPluginConfig = JSON.parse(newProviderData.plugin_config);
//   return {
//     ...newProviderData,
//     config: parsedConfig,
//     plugin_config: parsedPluginConfig,
//   };
// });

const validateData = () => {
  if (validate(newProviderData)) {
    console.log('valid');
  } else {
    errors.value = validate.errors || [];
    // console.log(validate.errors);
  }
};

const onChangeProvider = (value: string) => {
  // console.log('onChangeProvider', value);
};

const onChangeModel = (value: string) => {
  // console.log('onChangeModel', value);
};

const onChangePlugin = (event: any) => {
  setDefaultConfig(event.target.value, schema as SchemaConfig);
};

interface SchemaProperty {
  type?: string;
  default?: any;
  properties?: Record<string, SchemaProperty>;
  enum?: any[];
}

interface SchemaConfig {
  allOf: {
    if: {
      properties: {
        plugin?: { const: string };
      };
    };
    then: {
      properties: {
        config?: {
          type: string;
          properties: Record<string, SchemaProperty>;
        };
        plugin_config?: {
          type: string;
          properties: Record<string, SchemaProperty>;
        };
      };
    };
  }[];
}

function setDefaultConfig(plugin: string, schema: SchemaConfig): void {
  // Helper function to extract default values from the schema properties
  function extractDefaults(
    properties: Record<string, SchemaProperty>,
  ): Record<string, any> {
    const defaults: Record<string, any> = {};
    // console.log('properties', properties);
    Object.keys(properties).forEach((key) => {
      const prop = properties[key];
      // console.log('prop', prop);
      if ('default' in prop) {
        // console.log('found default', key);
        defaults[key] = prop.default;
      } else if (prop.type === 'object' && prop.properties) {
        // console.log('extracting defaults for', key);
        defaults[key] = extractDefaults(prop.properties);
      } else {
        defaults[key] = null;
      }
    });
    return defaults;
  }

  let configSchema: SchemaProperty | undefined;
  let pluginConfigSchema: SchemaProperty | undefined;

  schema.allOf.forEach((rule) => {
    if (rule.if?.properties?.plugin?.const === plugin) {
      console.log('rule', rule);
      configSchema = extractDefaults(
        rule.then.properties.config?.properties || {},
      );
      pluginConfigSchema = extractDefaults(
        rule.then.properties.plugin_config?.properties || {},
      );
    }
  });

  console.log({ configSchema });
  console.log({ pluginConfigSchema });

  newProviderData.config = configSchema ?? {};
  newProviderData.plugin_config = pluginConfigSchema ?? {};
}

const onChangePluginConfig = (value: any) => {
  // console.log('onChangePluginConfig', value);
};

const showPluginConfig = computed(() => {
  return !!newProviderData.plugin;
});

const showConfig = computed(() => {
  return !!newProviderData.plugin;
});
</script>

<template>
  <div>
    <FieldLabel for="provider">Provider:</FieldLabel>
    <TextInput
      id="provider"
      name="provider"
      v-model="newProviderData.provider"
      required
      testId="input-provider"
      @input="onChangeProvider"
    />
  </div>

  <div>
    <FieldLabel for="model">Model:</FieldLabel>
    <TextInput
      id="model"
      name="model"
      v-model="newProviderData.model"
      required
      testId="input-model"
      placeholder=""
      @input="onChangeModel"
    />
  </div>

  <div>
    <FieldLabel for="plugin">Plugin:</FieldLabel>
    <SelectInput
      id="plugin"
      name="plugin"
      v-model="newProviderData.plugin"
      :options="schema.properties.plugin.enum"
      required
      testId="input-plugin"
      @input="onChangePlugin"
    />
  </div>

  <div v-if="showPluginConfig">
    <FieldLabel>Plugin Config:</FieldLabel>
    <!-- <textarea name="" id="" v-model="newProviderData.plugin_config"></textarea> -->
    <div class="rounded-md bg-white p-2">
      <vue-json-pretty
        v-model:data="newProviderData.plugin_config"
        :editable="true"
        editableTrigger="click"
      />
    </div>
  </div>

  <div v-if="showConfig">
    <FieldLabel>Config:</FieldLabel>
    <!-- <textarea name="" id="" v-model="newProviderData.config"></textarea> -->
    <div class="rounded-md bg-white p-2">
      <vue-json-pretty
        v-model:data="newProviderData.config"
        :editable="true"
        editableTrigger="click"
      />
      {{ newProviderData.config }}
    </div>
  </div>

  <div v-for="error in validate.errors">
    {{ error.instancePath }}: {{ error.message }}
  </div>

  <button @click="validateData">Validate</button>
</template>

<style lang="css">
.vjs-tree * {
  font-size: 12px;
}
.vjs-tree input {
  outline: none;
  border: none !important;
  padding: 0 !important;
  &:focus {
    border: 2px solid red;
    outline: none;
  }
}
</style>
