import type {
  NodeLog,
  NewValidatorDataModel,
  ValidatorModel,
  RPCResponseEventData,
  TransactionStatusUpdateEventData,
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
  // const listenWebsocket = ref<boolean>(true);
  const contractsStore = useContractsStore();
  const nodeProviders = ref<Record<string, string[]>>({});
  const validators = ref<ValidatorModel[]>([]);
  const isLoadingValidatorData = ref<boolean>(true);

  if (!webSocketClient.connected) webSocketClient.connect();

  // TODO: Consider moving most of this to the backend and log everything there as well
  // TODO: add category to logs

  webSocketClient.on('genvm_deploy_contract', (data: any) => {
    addLog({
      category: 'GenVM',
      event: 'Deploy',
      type: 'info',
      message: 'Deploying contract',
      data: data,
    });
  });

  webSocketClient.on('genvm_run_contract', (data: any) => {
    addLog({
      category: 'GenVM',
      event: 'Write',
      type: 'info',
      message: 'Writing to contract',
      data: data,
    });
  });

  webSocketClient.on('genvm_read_contract', (data: any) => {
    addLog({
      category: 'GenVM',
      event: 'Read',
      type: 'info',
      message: data.method_name,
      data: data,
    });
  });

  webSocketClient.on('update_consensus_data', (data: RPCResponseEventData) => {
    addLog({
      category: 'Consensus',
      event: 'Consensus Update',
      type: 'info',
      message: 'xx',
      data: data,
    });
  });

  webSocketClient.on('rpc_response', (data: RPCResponseEventData) => {
    addLog({
      category: 'RPC',
      event: data.response.status === 'info' ? 'Called' : 'Response',
      type: data.response.status,
      message: data.function_name,
      data: data,
    });
  });

  // TODO: remake payloads for rpc calls and responses, split into two events
  // webSocketClient.on('rpc_call', (data: RPCResponseEventData) => {
  //   addLog({
  //     category: 'RPC',
  //     event: 'Called Endpoint',
  //     type: data.response.status,
  //     message: data.function_name,
  //     data: data,
  //   });
  // });

  webSocketClient.on(
    'transaction_status_update',
    (data: TransactionStatusUpdateEventData) => {
      // console.log('transaction_status_update', data);
      addLog({
        category: 'Transactions',
        event: 'Updated Transaction',
        type: 'info',
        message: data.new_status + ' ' + data.hash,
        data: data,
      });
    },
  );

  function addLog(log: NodeLog) {
    logs.value.push(log);
  }

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
        nodeProviders.value = modelsResult.data.reduce(
          (acc: Record<string, string[]>, llmprovider) => {
            const provider = llmprovider.provider;
            if (!acc[provider]) {
              acc[provider] = [];
            }
            acc[provider].push(llmprovider.model);
            return acc;
          },
          {},
        );
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
      throw new Error('Error udpating the validator');
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
      throw new Error('Error creating a new validator');
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

  return {
    logs,
    // listenWebsocket,
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

    validatorsOrderedById,
    hasAtLeastOneValidator,
  };
});
