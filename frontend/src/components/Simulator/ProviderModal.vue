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
// import { uniqBy } from 'lodash-es';
import Alert from '../global/Alert.vue';
import JsonForm from './JsonForm.vue';
const nodeStore = useNodeStore();
const { trackEvent } = useEventTracking();
const emit = defineEmits(['close']);
const error = ref('');
const isLoading = ref(false);
const props = defineProps<{
  provider?: ProviderModel;
}>();

const isCreateMode = computed(() => !props.provider);

async function handleCreateProvider() {
  error.value = '';
  isLoading.value = true;
  try {
    await nodeStore.addProvider(newProviderData.value);

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
    await nodeStore.updateProvider(provider, newProviderData.value);
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

const tryInitValues = () => {
  if (!props.provider) {
    // TODO: ?
    // try {
    //   newValidatorData.value.provider = nodeStore.nodeProviders[0].provider;
    //   handleChangeProvider();
    // } catch (err) {
    //   console.error('Could not initialize values', err);
    // }
  } else {
    newProviderData.value = {
      model: props.provider.model,
      provider: props.provider.provider,
      plugin: props.provider.plugin,
      config: JSON.stringify(props.provider.config, null, 2),
      plugin_config: JSON.stringify(props.provider.plugin_config, null, 2),
    };
  }
};
</script>

<template>
  <Modal @close="emit('close')" @onOpen="tryInitValues">
    <template #title v-if="isCreateMode">New Provider</template>
    <template #title v-else>Provider #{{ provider?.id }}</template>

    <JsonForm />
    <!--
    <Alert error v-if="error" type="error">{{ error }}</Alert>

    <Btn
      v-if="isCreateMode"
      @click="handleCreateProvider"
      :disabled="!providerModelValid"
      testId="btn-create-provider"
      :loading="isLoading"
    >
      Create
    </Btn>

    <Btn
      v-if="!isCreateMode && provider"
      @click="handleUpdateProvider(provider)"
      :disabled="!providerModelValid"
      testId="btn-update-provider"
      :loading="isLoading"
    >
      Save
    </Btn> -->
  </Modal>
</template>
