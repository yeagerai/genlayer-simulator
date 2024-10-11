<script setup lang="ts">
import { useNodeStore } from '@/stores';
import {
  type ValidatorModel,
  type NewValidatorDataModel,
  type ProviderModel,
} from '@/types';
import { notify } from '@kyvg/vue3-notification';
import { computed, ref } from 'vue';
import SelectInput from '@/components/global/inputs/SelectInput.vue';
import NumberInput from '@/components/global/inputs/NumberInput.vue';
import TextAreaInput from '@/components/global/inputs/TextAreaInput.vue';
import FieldError from '@/components/global/fields/FieldError.vue';
import FieldLabel from '@/components/global/fields/FieldLabel.vue';
import { useEventTracking } from '@/hooks';
import CopyTextButton from '../global/CopyTextButton.vue';
import { uniqBy } from 'lodash-es';
import Alert from '../global/Alert.vue';

// TODO: populate default config ?
// TODO: don't auto select invalid models/providers
// TODO: add config schema here

const nodeStore = useNodeStore();
const { trackEvent } = useEventTracking();
const emit = defineEmits(['close']);
const error = ref('');
const isLoading = ref(false);

const props = defineProps<{
  validator?: ValidatorModel;
}>();

const isCreateMode = computed(() => !props.validator);

async function handleCreateValidator() {
  error.value = '';
  isLoading.value = true;

  try {
    await nodeStore.createNewValidator(newValidatorData.value);

    notify({
      title: 'New validator created',
      type: 'success',
    });

    trackEvent('created_validator', {
      validator_provider: newValidatorData.value.provider,
      validator_model: newValidatorData.value.model,
      validator_stake: newValidatorData.value.stake,
    });

    emit('close');
  } catch (err) {
    console.error(err);
    error.value = (err as Error)?.message;
    // notify({
    //   title: 'Error',
    //   text: (error as Error)?.message || 'Error creating new validator',
    //   type: 'error',
    // });
  } finally {
    isLoading.value = false;
  }
}

async function handleUpdateValidator(validator: ValidatorModel) {
  error.value = '';
  isLoading.value = true;
  try {
    await nodeStore.updateValidator(validator, newValidatorData.value);
    notify({
      title: `Updated validator #${validator.id}`,
      type: 'success',
    });
    emit('close');
  } catch (err) {
    console.error(err);
    error.value = (err as Error)?.message;
    // notify({
    //   title: 'Error',
    //   text: (error as Error)?.message || 'Error udpating the validator',
    //   type: 'error',
    // });
  } finally {
    isLoading.value = false;
  }
}

const newValidatorData = ref<NewValidatorDataModel>({
  model: '',
  provider: '',
  stake: 1,
  config: '{ }',
});

const validatorModelValid = computed(() => {
  return (
    newValidatorData.value?.model !== '' &&
    newValidatorData.value?.provider !== '' &&
    newValidatorData.value?.stake > 0
  );
});

const isConfigValid = computed(() => {
  // Allow empty config
  if (!newValidatorData.value.config) {
    return true;
  }

  // Try to parse JSON
  try {
    JSON.parse(newValidatorData.value.config);
    return true;
  } catch (error) {
    return false;
  }
});

const providerOptions = computed(() => {
  return uniqBy(nodeStore.nodeProviders, 'provider').map((provider: any) => {
    return {
      label: provider.provider,
      value: provider.provider,
      disabled: !provider?.is_available,
    };
  });
});

const modelOptions = computed(() => {
  return uniqBy(nodeStore.nodeProviders, 'model')
    .filter(
      (provider: any) => provider.provider === newValidatorData.value.provider,
    )
    .map((provider: any) => {
      const isDisabled = !provider?.is_model_available;
      return {
        value: provider.model,
        label: isDisabled ? `${provider.model} (missing configuration)` : provider.model,
        disabled: !provider?.is_model_available,
      };
    });
});

const handleChangeProvider = () => {
  error.value = '';
  console.log('handleChangeProvider', newValidatorData.value.provider);
  const availableModels = nodeStore.availableModelsForProvider(
    newValidatorData.value.provider,
  );
  newValidatorData.value.model =
    availableModels.length > 0 ? availableModels[0] : '';
};

const handleChangeModel = () => {
  error.value = '';
  console.log('handleChangeModel', newValidatorData.value.model);
  console.log(nodeStore.nodeProviders);
  const config = nodeStore.nodeProviders.find(
    (provider: ProviderModel) =>
      provider.model === newValidatorData.value.model,
  )?.config;
  newValidatorData.value.config = JSON.stringify(config, null, 2);
};

const tryInitValues = () => {
  if (!props.validator) {
    try {
      newValidatorData.value.provider = nodeStore.nodeProviders[0].provider;
      handleChangeProvider();
    } catch (err) {
      console.error('Could not initialize values', err);
    }
  } else {
    newValidatorData.value = {
      model: props.validator.model,
      provider: props.validator.provider,
      stake: props.validator.stake,
      config: JSON.stringify(props.validator.config, null, 2),
    };
  }
};
</script>

<template>
  <Modal @close="emit('close')" @onOpen="tryInitValues">
    <template #title v-if="isCreateMode">New Validator</template>
    <template #title v-else>Validator #{{ validator?.id }}</template>

    <Alert warning v-if="providerOptions.length === 0">
      No node providers available. Please configure a provider first.
    </Alert>

    <template #info v-if="!isCreateMode">
      <div
        class="flex flex-row items-center gap-1 font-mono text-xs font-normal"
      >
        {{ validator?.address }}
        <CopyTextButton :text="validator?.address || ''" />
      </div>
    </template>

    <div>
      <FieldLabel for="provider">Provider:</FieldLabel>
      <SelectInput
        name="provider"
        :options="providerOptions"
        v-model="newValidatorData.provider"
        @change="handleChangeProvider"
        :invalid="!newValidatorData.provider"
        required
        testId="dropdown-provider"
        :disabled="providerOptions.length === 0"
      />
    </div>

    <div>
      <FieldLabel for="model">Model:</FieldLabel>
      <SelectInput
        name="model"
        :options="modelOptions"
        v-model="newValidatorData.model"
        @change="handleChangeModel"
        :invalid="!newValidatorData.model"
        required
        testId="dropdown-model"
        :disabled="providerOptions.length === 0"
      />

      <Alert
        warning
        class="mt-2"
        v-if="!newValidatorData.model && !!newValidatorData.provider"
        >No available models for this provider. Check your provider
        settings.</Alert
      >
    </div>

    <div>
      <FieldLabel for="stake">Stake:</FieldLabel>
      <NumberInput
        id="stake"
        name="stake"
        :min="1"
        :step="1"
        :invalid="newValidatorData.stake < 1"
        v-model="newValidatorData.stake"
        :forceInteger="true"
        required
        testId="input-stake"
      />
      <FieldError v-if="newValidatorData.stake < 1"
        >Please enter an integer greater than 0.</FieldError
      >
    </div>

    <div>
      <FieldLabel for="config">Config:</FieldLabel>
      <TextAreaInput
        id="config"
        name="config"
        :rows="5"
        :cols="60"
        v-model="newValidatorData.config"
        :invalid="!isConfigValid"
      />
      <FieldError v-if="!isConfigValid">Please enter valid JSON.</FieldError>
    </div>

    <Alert error v-if="error" type="error">{{ error }}</Alert>

    <Btn
      v-if="isCreateMode"
      @click="handleCreateValidator"
      :disabled="!validatorModelValid"
      testId="btn-create-validator"
      :loading="isLoading"
    >
      Create
    </Btn>

    <Btn
      v-if="!isCreateMode && validator"
      @click="handleUpdateValidator(validator)"
      :disabled="!validatorModelValid"
      testId="btn-update-validator"
      :loading="isLoading"
    >
      Save
    </Btn>
  </Modal>
</template>
