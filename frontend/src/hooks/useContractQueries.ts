import { watch, ref, onUnmounted, type Ref, inject, computed } from 'vue';
import type { IJsonRpcService } from '@/services';
import { useQuery, useQueryClient } from '@tanstack/vue-query';
import { deployContract } from 'viem/actions';
import type { ContractFile, DeployedContract, TransactionItem } from '@/types';
import {
  useContractsStore,
  useTransactionsStore,
  useAccountsStore,
} from '@/stores';
import { useDebounceFn } from '@vueuse/core';
import { notify } from '@kyvg/vue3-notification';

const schema = ref<any>();

export function useContractQueries() {
  console.log('useContractQueries');
  const $jsonRpc = inject<IJsonRpcService>('$jsonRpc'); // This could be done without inject/provide
  const accountsStore = useAccountsStore();
  const transactionsStore = useTransactionsStore();
  const queryClient = useQueryClient();
  let deploymentSubscription: () => void;

  const contractsStore = useContractsStore();
  const contract = computed(() => contractsStore.currentContract);

  const deployedContract = computed(() =>
    contractsStore.deployedContracts.find(
      ({ contractId }) => contractId === contract.value?.id,
    ),
  );

  const isDeployed = computed(() => !!deployedContract.value);
  // const className = ref<string>();

  // const address = ref<string>(''); // Provide a default value for address
  const address = computed(() => deployedContract.value?.address);
  // const constructorInputs = ref<{ [k: string]: string }>({});

  // const constructorInputs = computed<{ [k: string]: string }>(
  //   () => schema.value?.methods['__init__']?.inputs,
  // );

  // TODO: invalidate when code changes
  // TODO: debounce

  const fetchContractSchemaDebounced = useDebounceFn(() => {
    console.log('fetchContractSchemaDebounced');
    return fetchContractSchema();
  }, 300);

  watch(
    () => contract.value?.content,
    () => {
      console.log('changed');
      queryClient.invalidateQueries({
        queryKey: ['schema', contract.value?.id],
      });
    },
  );

  const contractSchemaQuery = useQuery({
    queryKey: [
      'schema',
      () => contract.value?.id,
      // () => contract.value?.content,
    ], // Better use key or manual invalidation on content change?
    queryFn: fetchContractSchemaDebounced,
    refetchOnWindowFocus: false,
    retry: 0,
    // enabled: () => !!contract.value
  });

  async function fetchContractSchema() {
    console.log('fetchContractSchema', contract.value);
    const result = await $jsonRpc?.getContractSchema({
      code: contract.value?.content ?? '',
    });
    console.log('fetchContractSchema result', result);
    if (result?.status === 'error') {
      throw new Error('Error fetching contract schema');
    }

    schema.value = result?.data;

    console.log('schema', schema.value);

    return schema.value;
  }

  const isDeploying = ref(false);

  async function deployContract({
    constructorParams,
  }: {
    constructorParams: { [k: string]: string };
  }) {
    isDeploying.value = true;

    // if (
    //   Object.keys({ ...constructorInputs.value }).length !==
    //   Object.keys(constructorParams).length
    // ) {
    //   throw new Error('You should provide a valid default state');
    // }

    try {
      const constructorParamsAsString = JSON.stringify(constructorParams);

      console.log(schema.value.class);
      const result = await $jsonRpc?.deployContract({
        userAccount: accountsStore.currentUserAddress || '',
        className: schema.value.class,
        code: contract.value?.content ?? '',
        constructorParams: constructorParamsAsString,
      });

      console.log('deploy result', result?.data);
      // address.value = result?.data.contract_address;

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

  return {
    contractSchemaQuery,
    contractAbiQuery,
    contract,

    schema,
    deployContract,
    // constructorInputs,
    isDeploying,
    isDeployed,
    address,
  };
}
