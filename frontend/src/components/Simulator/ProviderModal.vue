<script setup lang="ts">
import { useNodeStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import { useEventTracking } from '@/hooks';
import CopyTextButton from '../global/CopyTextButton.vue';
// import { uniqBy } from 'lodash-es';
import Alert from '../global/Alert.vue';
// import JsonForm from './JsonForm.vue';
import providerSchema from '../../../../backend/node/create_nodes/providers_schema.json';
// import { JsonForms } from '@jsonforms/vue';
// import { createAjv } from '@jsonforms/core';
import { vanillaRenderers } from '@jsonforms/vue-vanilla';
import {
  computed,
  defineComponent,
  markRaw,
  reactive,
  ref,
  onMounted,
  nextTick,
  watch,
} from 'vue';
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
import GhostBtn from '../global/GhostBtn.vue';
import { init } from '@jsonforms/core';

const nodeStore = useNodeStore();
const { trackEvent } = useEventTracking();
const emit = defineEmits(['close']);
const error = ref('');
const isLoading = ref(false);
const props = defineProps<{
  provider?: ProviderModel;
}>();

// TODO: test state across modals (reset errors on open?)

const isCreateMode = computed(() => !props.provider);

async function handleCreateProvider() {
  error.value = '';
  isLoading.value = true;
  try {
    await nodeStore.addProvider(newProviderData);

    notify({
      title: 'Added new provider',
      type: 'success',
    });

    // TODO:
    // trackEvent('created_provider', {
    //   provider_provider: newProviderData.value.provider,
    //   provider_model: newProviderData.value.model,
    //   provider_stake: newProviderData.value.stake,
    // });

    emit('close');
  } catch (err) {
    console.error(err);
    error.value = (err as Error)?.message;
    // notify({
    //   title: 'Error',
    //   text: (err as Error)?.message || 'Error adding provider',
    //   type: 'error',
    // });
  } finally {
    isLoading.value = false;
  }
}

async function handleUpdateProvider(provider: ProviderModel) {
  error.value = '';
  isLoading.value = true;
  try {
    await nodeStore.updateProvider(provider, newProviderData);
    notify({
      title: `Updated ${provider.model}`,
      type: 'success',
    });
    emit('close');
  } catch (err) {
    console.error(err);
    error.value = (err as Error)?.message;
    // notify({
    //   title: 'Error',
    //   text: (error as Error)?.message || 'Error udpating the provider',
    //   type: 'error',
    // });
  } finally {
    isLoading.value = false;
  }
}

const ajv = new Ajv2020({
  allErrors: false,
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

const validate = ajv.compile(schema);
const errors = ref<any[]>([]);
const pluginOptions = ref<string[]>([]);
const modelOptions = ref<string[]>([]);
const isPluginLocked = ref(false);
const customProvider = ref(false);
const providerOptions = ref<string[]>([]);

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

const tryInitValues = () => {
  initProvider();

  checkRules();
  // pluginOptions.value = schema.properties.plugin.enum;
  // const initialPlugin = pluginOptions.value[0];

  // if (initialPlugin) {
  //   newProviderData.plugin = initialPlugin;
  //   onChangePlugin(initialPlugin);
  // }
};

const initProvider = () => {
  providerOptions.value = schema.properties.provider.examples;
  const initialProvider = 'openai';
  newProviderData.provider = initialProvider;
};

// 1. If provider == "ollama" then plugin must be "ollama"
// 2. If provider == "heuristai" then plugin = "openai" AND model is restricted to specific options
// 3. If provider == "openai" then plugin = "openai" AND model is limited to specific GPT versions
// 4. If provider == "anthropic" then plugin = "anthropic" AND model is restricted to Claude versions

// 5. If plugin == "ollama" then define specific plugin_config and config options
// 6. If plugin == "openai" then set plugin_config (API key, URL) and config (temperature, max_tokens)
// 7. If plugin == "anthropic" then configure plugin_config (API key, URL) and config (various generation parameters)

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

const checkRules = () => {
  console.log('checkRules');
  isPluginLocked.value = false;
  modelOptions.value = [];
  newProviderData.model = '';

  schema.allOf.forEach((rule) => {
    // Provider rules
    if (rule.if?.properties?.provider?.const === newProviderData.provider) {
      if (rule.then?.properties?.plugin?.const) {
        console.log('plugin locked');
        newProviderData.plugin = rule.then?.properties?.plugin?.const;
        isPluginLocked.value = true;
      }

      if (rule.then?.properties?.model?.enum) {
        modelOptions.value = rule.then?.properties?.model?.enum;
        console.log(rule.then?.properties?.model?.enum[0]);
        newProviderData.model = rule.then?.properties?.model?.enum[0];
        // re-check
      }
    }

    // Plugin rules
    if (rule.if?.properties?.plugin?.const === newProviderData.plugin) {
      const pluginConfigProperties =
        rule.then?.properties?.plugin_config?.properties || {};
      const pluginConfig = extractDefaults(pluginConfigProperties);
      newProviderData.plugin_config = pluginConfig ? { ...pluginConfig } : {};

      const configProperties = rule.then?.properties?.config?.properties || {};
      const config = extractDefaults(configProperties);
      newProviderData.config = config ? { ...config } : {};
    }
  });
};

const toggleCustomProvider = () => {
  customProvider.value = !customProvider.value;
  if (customProvider.value) {
    newProviderData.provider = '';
  } else {
    initProvider();
  }
  checkRules();
};

const validateData = async () => {
  console.log('validateData', newProviderData.plugin_config);
  const res = validate(newProviderData);
  console.log(res);
  // console.log('validateData', newProviderData, res, validate);
  if (res) {
    errors.value = [];
    console.log('valid');
  } else {
    errors.value = validate.errors || [];
    console.log('not valid');

    // console.log(validate.errors);
  }
};

const onChangeModel = (value: string) => {
  // console.log('onChangeModel', value);
};

const onChangeField = () => {
  validateData();
};

watch(
  () => newProviderData.plugin,
  (plugin: string) => {
    setDefaultConfig(plugin, schema as SchemaConfig);
    validateData();
  },
);
// const onChangePlugin = async (plugin: string) => {
//   setDefaultConfig(plugin, schema as SchemaConfig);
//   validateData();
// };

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
    console.log('rule', rule);

    if (rule.if?.properties?.plugin?.const === plugin) {
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
  <Modal @close="emit('close')" @onOpen="tryInitValues">
    <template #title v-if="isCreateMode">New Provider Config</template>
    <template #title v-else>Provider Config #{{ provider?.id }}</template>

    <div>
      <div class="flex justify-between">
        <FieldLabel for="provider">Provider:</FieldLabel>

        <button
          @click="toggleCustomProvider"
          class="mr-1 text-xs opacity-50 hover:opacity-70"
        >
          {{ customProvider ? 'Use preset' : 'Custom provider' }}
        </button>
      </div>

      <TextInput
        id="provider"
        v-if="customProvider"
        name="provider"
        v-model="newProviderData.provider"
        required
        testId="input-provider"
        @update:modelValue="checkRules"
        :placeholder="'ex: ' + schema.properties.provider.examples.join(', ')"
      />
      <SelectInput
        v-else
        id="provider"
        name="provider"
        v-model="newProviderData.provider"
        required
        :options="providerOptions"
        testId="input-provider"
        @update:modelValue="checkRules"
        :placeholder="'ex: ' + schema.properties.provider.examples.join(', ')"
      />
    </div>

    <div>
      <FieldLabel for="model">Model:</FieldLabel>
      <TextInput
        v-if="modelOptions.length === 0"
        id="model"
        name="model"
        v-model="newProviderData.model"
        required
        testId="input-model"
        placeholder=""
        @input="onChangeModel"
      />
      <SelectInput
        v-if="modelOptions.length > 0"
        id="plugin"
        name="plugin"
        v-model="newProviderData.model"
        :options="modelOptions"
        required
        testId="input-model"
        @update:modelValue="onChangeModel"
      />
    </div>

    <div v-if="!isPluginLocked">
      <FieldLabel for="plugin">Plugin:</FieldLabel>
      <SelectInput
        id="plugin"
        name="plugin"
        v-model="newProviderData.plugin"
        :options="schema.properties.plugin.enum"
        :disabled="isPluginLocked"
        required
        testId="input-plugin"
        @update:modelValue="onChangePlugin"
      />
    </div>

    <div v-if="showPluginConfig">
      <FieldLabel>Provider Config:</FieldLabel>

      <div v-for="key in Object.keys(newProviderData.plugin_config)">
        {{ key }}:
        <input
          type="text"
          v-model="newProviderData.plugin_config[key]"
          @input="onChangeField"
        />
      </div>
      <!-- <textarea name="" id="" v-model="newProviderData.plugin_config"></textarea> -->
      <!-- <div class="rounded-md bg-white p-2">
      <vue-json-pretty
        v-model:data="newProviderData.plugin_config"
        :editable="true"
        editableTrigger="click"
      />
    </div> -->
      {{ newProviderData.plugin_config }}
    </div>

    <div v-if="showConfig">
      <FieldLabel>Default Validator Config:</FieldLabel>
      <!-- <textarea name="" id="" v-model="newProviderData.config"></textarea> -->
      <div class="rounded-md bg-white p-2">
        <vue-json-pretty
          v-model:data="newProviderData.config"
          :editable="true"
          editableTrigger="click"
        />
      </div>
    </div>

    <div v-for="error in errors" class="text-xs text-red-500">
      <!-- {{ error }} -->
      {{ error.instancePath }}: {{ error.message }}
    </div>

    <button @click="validateData">Validate</button>

    <Alert error v-if="error" type="error">{{ error }}</Alert>

    <Btn
      v-if="isCreateMode"
      @click="handleCreateProvider"
      :disabled="errors.length > 0"
      testId="btn-create-provider"
      :loading="isLoading"
    >
      Create
    </Btn>

    <Btn
      v-if="!isCreateMode && provider"
      @click="handleUpdateProvider(provider)"
      :disabled="errors.length > 0"
      testId="btn-update-provider"
      :loading="isLoading"
    >
      Save
    </Btn>
  </Modal>
</template>
