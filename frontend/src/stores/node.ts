import type {
  NodeLog,
  NewValidatorDataModel,
  ValidatorModel,
  GetProvidersAndModelsData,
  NewProviderDataModel,
  ProviderModel,
} from '@/types';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { useContractsStore } from './contracts';
import { notify } from '@kyvg/vue3-notification';
import { useRpcClient, useWebSocketClient } from '@/hooks';

export const useNodeStore = defineStore('nodeStore', () => {
  const rpcClient = useRpcClient();
  const webSocketClient = useWebSocketClient();
  const logs = ref<NodeLog[]>([]);
  const listenWebsocket = ref<boolean>(true);
  const contractsStore = useContractsStore();
  const nodeProviders = ref<GetProvidersAndModelsData>([]);
  // state
  const validators = ref<ValidatorModel[]>([]);
  const isLoadingValidatorData = ref<boolean>(true);

  if (!webSocketClient.connected) webSocketClient.connect();
  webSocketClient.on('status_update', (event) => {
    if (listenWebsocket.value) {
      if (event.message?.function !== 'get_transaction_by_hash') {
        if (event.message?.function === 'intelligent_contract_execution') {
          const executionLogs: string[] =
            event.message.response.message.split('\n\n');
          executionLogs
            .filter((log: string) => log.trim().length > 0)
            .forEach((log: string) => {
              logs.value.push({
                date: new Date().toISOString(),
                message: {
                  function: 'Intelligent Contract Execution Log',
                  trace_id: String(Math.random() * 100),
                  response: {
                    status: 'contractLog',
                    message: log,
                  },
                },
              });
            });
        } else {
          logs.value.push({
            date: new Date().toISOString(),
            message: event.message,
          });
        }
      }
    }
  });

  async function getValidatorsData() {
    isLoadingValidatorData.value = true;

    try {
      const [validatorsResult, modelsResult] = await Promise.all([
        rpcClient.getValidators(),
        rpcClient.getProvidersAndModels(),
      ]);

      if (validatorsResult?.status === 'success') {
        validators.value = validatorsResult.data;
      } else {
        throw new Error('Error getting validators');
      }

      if (modelsResult?.status === 'success') {
        console.log(modelsResult);
        nodeProviders.value = modelsResult.data;
      } else {
        throw new Error('Error getting Providers and Models data');
      }
    } catch (error) {
      console.error(error);
      notify({
        title: 'Error',
        text: (error as Error)?.message || 'Error loading validators',
        type: 'error',
      });
    } finally {
      isLoadingValidatorData.value = false;
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
    const result = await rpcClient.updateValidator({
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
      // TODO: better normalize error handling
      if (result.exception) {
        throw new Error(result.exception);
      } else {
        throw new Error(result.message);
      }
    }
  }

  const deleteValidator = async (validator: ValidatorModel) => {
    if (validators.value.length === 1) {
      throw new Error('You must have at least one validator');
    }
    const result = await rpcClient.deleteValidator({
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
    const result = await rpcClient.createValidator({
      stake,
      provider,
      model,
      config: validatorConfig,
    });
    if (result?.status === 'success') {
      validators.value.push(result.data);
    } else {
      // TODO: better normalize error handling
      if (result.exception) {
        throw new Error(result.exception);
      } else {
        throw new Error(result.message);
      }
    }
  }

  async function cloneValidator(validator: ValidatorModel) {
    const result = await rpcClient.createValidator(validator);
    if (result?.status === 'success') {
      validators.value.push(result.data);
    } else {
      throw new Error('Error cloning validator');
    }
  }

  async function addProvider(providerData: NewProviderDataModel) {
    const result = await rpcClient.addProvider({
      ...providerData,
      plugin_config: JSON.parse(providerData.plugin_config),
      config: JSON.parse(providerData.config),
    });
    console.log(result);
    if (result?.status === 'success') {
      // nodeProviders.value.push(result.data);
      getValidatorsData();
    } else {
      if (result.exception) {
        throw new Error(result.exception);
      } else {
        throw new Error(result.message);
      }
    }
  }

  async function updateProvider(
    provider: ProviderModel,
    newProviderData: NewProviderDataModel,
  ) {
    const result = await rpcClient.updateProvider({
      id: provider.id,
      ...newProviderData,
      config: JSON.parse(newProviderData.config),
      plugin_config: JSON.parse(newProviderData.plugin_config),
    });
    if (result?.status === 'success') {
      getValidatorsData();
    } else {
      if (result.exception) {
        throw new Error(result.exception);
      } else {
        throw new Error(result.message);
      }
    }
  }

  async function deleteProvider(id: number) {
    const result = await rpcClient.deleteProvider({ id });
    console.log(result);
    if (result?.status === 'success') {
      // nodeProviders.value = nodeProviders.value.filter((provider) => provider.id !== id);
      getValidatorsData();
    } else {
      throw new Error('Error adding provider');
    }
  }

  const contractsToDelete = computed(() =>
    contractsStore.contracts.filter((c) => c.example),
  );

  const validatorsOrderedById = computed(() =>
    validators.value.slice().sort((a, b) => a.id - b.id),
  );

  const clearLogs = () => {
    logs.value = [];
  };

  const hasAtLeastOneValidator = computed(() => validators.value.length >= 1);

  const availableProviders = computed(() => [
    ...new Set(
      nodeProviders.value
        .filter((provider) => provider.is_available)
        .map((provider) => provider.provider),
    ),
  ]);

  const availableModelsForProvider = computed(
    () => (selectedProvider: string) => [
      ...new Set(
        nodeProviders.value
          .filter(
            (provider) =>
              provider.is_model_available &&
              provider.provider === selectedProvider,
          )
          .map((provider) => provider.model),
      ),
    ],
  );

  return {
    logs,
    listenWebsocket,
    validators,
    nodeProviders,
    contractsToDelete,
    isLoadingValidatorData,

    getValidatorsData,
    createNewValidator,
    cloneValidator,
    deleteValidator,
    updateValidator,
    clearLogs,
    addProvider,
    updateProvider,
    deleteProvider,

    availableProviders,
    availableModelsForProvider,
    validatorsOrderedById,
    hasAtLeastOneValidator,
  };
});
