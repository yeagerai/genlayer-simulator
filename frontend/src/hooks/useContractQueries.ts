import { watch, ref, inject, computed } from 'vue';
import type { IJsonRpcService } from '@/services';
import { useQuery, useQueryClient } from '@tanstack/vue-query';
import type { TransactionItem } from '@/types';
import {
  useContractsStore,
  useTransactionsStore,
  useAccountsStore,
} from '@/stores';
import { useDebounceFn } from '@vueuse/core';
import { notify } from '@kyvg/vue3-notification';

// TODO: review why we need this scoped here again
const schema = ref<any>();

export function useContractQueries() {
  console.log('useContractQueries');
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc'); // This could be done without inject/provide
  const accountsStore = useAccountsStore();
  const transactionsStore = useTransactionsStore();
  const contractsStore = useContractsStore();
  const queryClient = useQueryClient();
  const contract = computed(() => contractsStore.currentContract);

  const deployedContract = computed(() =>
    contractsStore.deployedContracts.find(
      ({ contractId }) => contractId === contract.value?.id,
    ),
  );

  const isDeployed = computed(() => !!deployedContract.value);
  const address = computed(() => deployedContract.value?.address);

  const fetchContractSchemaDebounced = useDebounceFn(() => {
    console.log('fetchContractSchemaDebounced');
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
    const result = await $jsonRpc?.getContractSchema({
      code: contract.value?.content ?? '',
    });

    if (result?.status === 'error') {
      throw new Error('Error fetching contract schema');
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
      const constructorParamsAsString = JSON.stringify(constructorParams);

      const result = await $jsonRpc?.deployContract({
        userAccount: accountsStore.currentUserAddress || '',
        className: schema.value.class,
        code: contract.value?.content ?? '',
        constructorParams: constructorParamsAsString,
      });

      if (result?.status === 'success') {
        const tx: TransactionItem = {
          contractAddress: result?.data.contract_address,
          localContractId: contract.value?.id ?? '',
          txId: result?.data.transaction_id,
          type: 'deploy',
          status: 'PENDING',
          data: {},
        };

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

  const contractAbiQuery = useQuery({
    queryKey: [
      'abi',
      () => contract.value?.id,
      () => deployedContract.value?.address,
    ],
    queryFn: fetchContractAbi,
    enabled: isDeployed,
    refetchOnWindowFocus: false,
    retry: 2,
  });

  async function fetchContractAbi() {
    console.log('fetchContractAbi', address.value);
    const result = await $jsonRpc?.getDeployedContractSchema({
      address: deployedContract.value?.address ?? '',
    });
    // Handle errors here?
    return result?.data;
  }

  // TODO: review error handling
  // TODO: add error in method UI
  async function callReadMethod(method: string, methodArguments: string[]) {
    try {
      const result = await $jsonRpc?.getContractState({
        contractAddress: address.value || '',
        method,
        methodArguments,
      });

      if (result?.status === 'error') {
        throw new Error(result.message);
      }

      console.log('result', result);

      // TODO: re-use this?
      // currentContractState.value = {
      //   ...currentContractState.value,
      //   [method]: result?.data,
      // };

      return result?.data;
    } catch (error) {
      console.error(error);
      throw new Error('Error getting the contract state');
    }
  }

  async function callWriteMethod({
    userAccount,
    method,
    params,
  }: {
    userAccount: string;
    method: string;
    params: any[];
  }) {
    try {
      const result = await $jsonRpc?.callContractFunction({
        userAccount,
        contractAddress: address.value || '',
        method,
        params,
      });

      // TODO: Check potential race condition issue on contract id
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
    }
    return false;
  }

  return {
    contractSchemaQuery,
    contractAbiQuery,
    contract,
    deployContract,
    isDeploying,
    isDeployed,
    address,

    callReadMethod,
    callWriteMethod,
  };
}
