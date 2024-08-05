import type { IJsonRpcService } from '@/services';
import type { NodeLog, NewValidatorDataModel, ValidatorModel } from '@/types';
import { webSocketClient } from '@/utils';
import { defineStore } from 'pinia';
import { computed, inject, ref } from 'vue';
import { useContractsStore } from './contracts';

export const useNodeStore = defineStore('nodeStore', () => {
  const logs = ref<NodeLog[]>([]);
  const listenWebsocket = ref<boolean>(true);
  const contractsStore = useContractsStore();
  const nodeProviders = ref<Record<string, string[]>>({});
  // state
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc')!;
  const validators = ref<ValidatorModel[]>([]);

  if (!webSocketClient.connected) webSocketClient.connect();
  webSocketClient.on('status_update', (event) => {
    if (listenWebsocket.value) {
      if (event.message?.function !== 'get_transaction_by_id') {
        logs.value.push({
          date: new Date().toISOString(),
          message: event.message,
        });
      }
    }
  });

  async function getValidatorsData() {
    const [validatorsResult, modelsResult] = await Promise.all([
      $jsonRpc.getValidators(),
      $jsonRpc.getProvidersAndModels(),
    ]);

    if (validatorsResult?.status === 'success') {
      validators.value = validatorsResult.data;
    } else {
      throw new Error('Error getting validators');
    }

    if (modelsResult?.status === 'success') {
      nodeProviders.value = modelsResult.data;
    } else {
      throw new Error('Error getting Providers and Models data');
    }
  }

  async function updateValidator(
    validator: ValidatorModel,
    newValidatorData: NewValidatorDataModel,
  ) {
    const { stake, provider, model, config } = newValidatorData;

    if (stake <= 0 || !provider || !model || !config) {
      throw new Error('Please fill all the required fields');
    }
    const validatorConfig = JSON.parse(config || '{}');
    const result = await $jsonRpc.updateValidator({
      address: validator.address || '',
      stake,
      provider,
      model,
      config: validatorConfig,
    });
    if (result?.status === 'success') {
      const index = validators.value.findIndex(
        (v) => v.address === validator.address,
      );

      if (index >= 0) {
        validators.value.splice(index, 1, result.data);
      }
    } else {
      throw new Error('Error udpating the validator');
    }
  }

  const deleteValidator = async (validator: ValidatorModel) => {
    if (validators.value.length === 1) {
      throw new Error('You must have at least one validator');
    }
    const result = await $jsonRpc.deleteValidator({
      address: validator.address || '',
    });
    if (result?.status === 'success') {
      validators.value = validators.value.filter(
        (v) => v.address !== validator.address,
      );
    } else {
      throw new Error('Error deleting the validator');
    }
  };

  async function createNewValidator(newValidatorData: NewValidatorDataModel) {
    const { stake, provider, model, config } = newValidatorData;
    const validatorConfig = JSON.parse(config || '{}');
    const result = await $jsonRpc.createValidator({
      stake,
      provider,
      model,
      config: validatorConfig,
    });
    if (result?.status === 'success') {
      validators.value.push(result.data);
    } else {
      throw new Error('Error creating a new validator');
    }
  }

  const contractsToDelete = computed(() =>
    contractsStore.contracts.filter(
      (c) => (c.example && !c.updatedAt) || (!c.example && !c.updatedAt),
    ),
  );

  return {
    logs,
    listenWebsocket,
    validators,
    nodeProviders,
    contractsToDelete,

    getValidatorsData,
    createNewValidator,
    deleteValidator,
    updateValidator,
  };
});
