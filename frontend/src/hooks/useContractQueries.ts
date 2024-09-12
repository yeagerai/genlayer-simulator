import { watch, ref, computed } from 'vue';
import { useQuery, useQueryClient } from '@tanstack/vue-query';
import type { Address, TransactionItem } from '@/types';
import {
  useContractsStore,
  useTransactionsStore,
  useAccountsStore,
} from '@/stores';
import { useDebounceFn } from '@vueuse/core';
import { notify } from '@kyvg/vue3-notification';
import { useMockContractData } from './useMockContractData';
import { useEventTracking, useRpcClient, useWallet } from '@/hooks';

const schema = ref<any>();

export function useContractQueries() {
  const rpcClient = useRpcClient();
  const accountsStore = useAccountsStore();
  const transactionsStore = useTransactionsStore();
  const contractsStore = useContractsStore();
  const queryClient = useQueryClient();
  const { trackEvent } = useEventTracking();
  const wallet = useWallet();
  const contract = computed(() => contractsStore.currentContract);

  const { mockContractId, mockContractSchema } = useMockContractData();

  const isMock = computed(() => contract.value?.id === mockContractId);

  const deployedContract = computed(() =>
    contractsStore.deployedContracts.find(
      ({ contractId }) => contractId === contract.value?.id,
    ),
  );

  const isDeployed = computed(() => !!deployedContract.value);
  const address = computed(() => deployedContract.value?.address);

  const fetchContractSchemaDebounced = useDebounceFn(() => {
    return fetchContractSchema();
  }, 300);

  watch(
    () => contract.value?.content,
    () => {
      queryClient.invalidateQueries({
        queryKey: ['schema', contract.value?.id],
      });
    },
  );

  const contractSchemaQuery = useQuery({
    queryKey: ['schema', () => contract.value?.id],
    queryFn: fetchContractSchemaDebounced,
    refetchOnWindowFocus: false,
    retry: 0,
    enabled: !!contract.value?.id,
  });

  async function fetchContractSchema() {
    if (isMock.value) {
      return mockContractSchema;
    }

    const result = await rpcClient.getContractSchema({
      code: contract.value?.content ?? '',
    });

    if (result?.status === 'error') {
      throw new Error(result?.message || 'Error fetching contract schema');
    }

    schema.value = result?.data;

    return schema.value;
  }

  const isDeploying = ref(false);

  async function deployContract({
    constructorParams,
  }: {
    constructorParams: { [k: string]: string };
  }) {
    isDeploying.value = true;

    try {
      if (!contract.value || !accountsStore.currentPrivateKey) {
        throw new Error('Error Deploying the contract');
      }
      const constructorParamsAsString = JSON.stringify(constructorParams);
      const data = [contract.value?.content ?? '', constructorParamsAsString];
      const signed = await wallet.signTransaction({
        privateKey: accountsStore.currentPrivateKey,
        data,
      });
      const result = await rpcClient.sendTransaction(signed);

      if (result?.status === 'success') {
        const tx: TransactionItem = {
          contractAddress: result?.data.contract_address,
          localContractId: contract.value?.id ?? '',
          txId: result?.data.transaction_id,
          type: 'deploy',
          status: 'PENDING',
          data: {},
        };

        notify({
          title: 'Started deploying contract',
          type: 'success',
        });

        trackEvent('deployed_contract', {
          contract_name: contract.value?.name || '',
        });

        transactionsStore.clearTransactionsForContract(
          contract.value?.id ?? '',
        );
        transactionsStore.addTransaction(tx);

        return tx;
      } else {
        throw new Error(
          typeof result?.message === 'string'
            ? result.message
            : 'Error Deploying the contract',
        );
      }
    } catch (error) {
      isDeploying.value = false;
      console.error(error);
      notify({
        type: 'error',
        title: 'Error deploying contract',
      });
      throw new Error('Error Deploying the contract');
    }
  }

  const abiQueryEnabled = computed(
    () => !!contract.value && !!isDeployed.value,
  );

  const contractAbiQuery = useQuery({
    queryKey: [
      'abi',
      () => contract.value?.id,
      () => deployedContract.value?.address,
    ],
    queryFn: fetchContractAbi,
    enabled: abiQueryEnabled,
    refetchOnWindowFocus: false,
    retry: 2,
  });

  async function fetchContractAbi() {
    if (isMock.value) {
      return mockContractSchema;
    }

    const result = await rpcClient.getDeployedContractSchema({
      address: deployedContract.value?.address ?? '',
    });

    if (result?.status === 'error') {
      console.error(result.message);
      throw new Error('Error fetching contract abi');
    }

    return result?.data;
  }

  async function callReadMethod(method: string, methodArguments: string[]) {
    try {
      const methodParamsAsString = JSON.stringify(methodArguments);
      const data = [method, methodParamsAsString];
      const encodedData = wallet.encodeTransactionData(data);

      const result = await rpcClient.getContractState({
        contractAddress: address.value || '',
        userAccount: accountsStore.currentUserAddress,
        data: encodedData,
      });

      if (result?.status === 'error') {
        console.error(result.message);
        throw new Error(result.message);
      }

      return result?.data;
    } catch (error) {
      console.error(error);
      throw new Error('Error getting the contract state');
    }
  }

  async function callWriteMethod({
    method,
    params,
  }: {
    method: string;
    params: any[];
  }) {
    try {
      if (!accountsStore.currentPrivateKey) {
        throw new Error('Error Deploying the contract');
      }
      const methodParamsAsString = JSON.stringify(params);
      const data = [method, methodParamsAsString];
      const to = (address.value as Address) || null;

      const signed = await wallet.signTransaction({
        privateKey: accountsStore.currentPrivateKey,
        data,
        to,
      });

      const result = await rpcClient.sendTransaction(signed);

      if (result?.status === 'success') {
        transactionsStore.addTransaction({
          contractAddress: address.value || '',
          localContractId: contract.value?.id || '',
          txId: (result?.data as any).transaction_id,
          type: 'method',
          status: 'PENDING',
          data: {},
        });

        return true;
      }
    } catch (error) {
      console.error(error);
      throw new Error('Error writing to contract');
    }
    return false;
  }

  return {
    contractSchemaQuery,
    contractAbiQuery,
    contract,
    isDeploying,
    isDeployed,
    address,

    deployContract,
    callReadMethod,
    callWriteMethod,

    mockContractSchema,
    isMock,
  };
}
