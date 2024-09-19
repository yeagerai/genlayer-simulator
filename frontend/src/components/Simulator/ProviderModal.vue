<script setup lang="ts">
import { useNodeStore } from '@/stores';
import { type ProviderModel, type NewProviderDataModel } from '@/types';
import { notify } from '@kyvg/vue3-notification';
import { computed, ref } from 'vue';
import TextInput from '@/components/global/inputs/TextInput.vue';
import SelectInput from '@/components/global/inputs/SelectInput.vue';
import NumberInput from '@/components/global/inputs/NumberInput.vue';
import TextAreaInput from '@/components/global/inputs/TextAreaInput.vue';
import FieldError from '@/components/global/fields/FieldError.vue';
import FieldLabel from '@/components/global/fields/FieldLabel.vue';
import { useEventTracking } from '@/hooks';
import CopyTextButton from '../global/CopyTextButton.vue';
import { uniqBy } from 'lodash-es';
import Alert from '../global/Alert.vue';

const nodeStore = useNodeStore();
const { trackEvent } = useEventTracking();
const emit = defineEmits(['close']);
const error = ref('');

const props = defineProps<{
  provider?: ProviderModel;
}>();

const isCreateMode = computed(() => !props.provider);

async function handleCreateProvider() {
  try {
    const data = { ...newProviderData.value };
    data.config = JSON.parse(data.config);
    data.plugin_config = JSON.parse(data.plugin_config);
    await nodeStore.addProvider(data);

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
  }
}

async function handleUpdateProvider(provider: ProviderModel) {
  try {
    await nodeStore.updateProvider(newProviderData.value);
    notify({
      title: `Updated ${provider.model}`,
      type: 'success',
    });
    emit('close');
  } catch (error) {
    console.error(error);
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error udpating the provider',
      type: 'error',
    });
  }
}

const newProviderData = ref<NewProviderDataModel>({
  model: 'test',
  provider: 'test',
  config: '{}',
  plugin: 'test',
  plugin_config: '{}',
  // plugin_config: {
  //   api_key_env_var: '',
  //   api_url: null,
  // },
});

// TODO:
const providerModelValid = computed(() => {
  return (
    newProviderData.value?.model !== '' &&
    newProviderData.value?.provider !== '' &&
    newProviderData.value?.plugin !== ''
  );
});

const isPluginConfigValid = computed(() => {
  // Allow empty config
  if (!newProviderData.value.plugin_config) {
    return true;
  }

  // Try to parse JSON
  try {
    JSON.parse(newProviderData.value.plugin_config);
    return true;
  } catch (error) {
    return false;
  }
});

const isConfigValid = computed(() => {
  // Allow empty config
  if (!newProviderData.value.config) {
    return true;
  }

  // Try to parse JSON
  try {
    JSON.parse(newProviderData.value.config);
    return true;
  } catch (error) {
    return false;
  }
});
</script>

<template>
  <Modal @close="emit('close')">
    <template #title v-if="isCreateMode">New Provider</template>
    <template #title v-else>Provider #{{ provider?.id }}</template>

    <div>
      <FieldLabel for="provider">Provider:</FieldLabel>
      <TextInput
        id="provider"
        name="provider"
        v-model="newProviderData.provider"
        required
        testId="input-provider"
        placeholder="openai, ollama..."
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
        placeholder="gpt-4o-mini, llama3-70b..."
      />
    </div>

    <div>
      <FieldLabel for="plugin">Plugin:</FieldLabel>
      <TextInput
        id="plugin"
        name="plugin"
        v-model="newProviderData.plugin"
        required
        testId="input-plugin"
        placeholder=""
      />
    </div>

    <div>
      <FieldLabel for="plugin-config">Plugin Config:</FieldLabel>
      <TextAreaInput
        id="plugin-config"
        name="plugin-config"
        :rows="5"
        :cols="60"
        v-model="newProviderData.plugin_config"
        :invalid="!isPluginConfigValid"
      />
      <FieldError v-if="!isConfigValid">Please enter valid JSON.</FieldError>
    </div>

    <div>
      <FieldLabel for="config">Config:</FieldLabel>
      <TextAreaInput
        id="config"
        name="config"
        :rows="5"
        :cols="60"
        v-model="newProviderData.config"
        :invalid="!isConfigValid"
      />
      <FieldError v-if="!isConfigValid">Please enter valid JSON.</FieldError>
    </div>

    <Alert v-if="error" type="error">{{ error }}</Alert>

    <Btn
      v-if="isCreateMode"
      @click="handleCreateProvider"
      :disabled="!providerModelValid"
      testId="btn-create-provider"
    >
      Create
    </Btn>

    <Btn
      v-if="!isCreateMode && provider"
      @click="handleUpdateProvider(provider)"
      :disabled="!providerModelValid"
      testId="btn-update-provider"
    >
      Save
    </Btn>
  </Modal>
</template>
