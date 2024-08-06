<script setup lang="ts">
import type { ContractMethod } from '@/types';
import { ref, computed } from 'vue';
import { Collapse } from 'vue-collapsed';
import { InputTypesMap } from '@/utils';
import { useContractsStore, useAccountsStore } from '@/stores';
import { notify } from '@kyvg/vue3-notification';
import { ChevronDownIcon } from '@heroicons/vue/16/solid';
const accountsStore = useAccountsStore();
const contractsStore = useContractsStore();

const props = defineProps<{
  methodName: string;
  method: ContractMethod;
  methodType: 'read' | 'write';
}>();

const isExpanded = ref(false);

// TODO: fix e2e tests

// const inputs = computed<{ [k: string]: any }>(() => {
//     return props.methods.reduce((prev: any, curr) => {
//         prev[curr.name] = {}
//         return prev
//     }, {})
// })

const inputs = ref<{ [k: string]: any }>({});

// const handleCallContractMethod = async ({
//   method,
//   params,
// }: {
//   method: string;
//   params: any[];
// }) => {
//   const result = await contractsStore.callContractMethod({
//     userAccount: accountsStore.currentUserAddress || '',
//     localContractId: contractsStore.deployedContract?.contractId || '',
//     method: `${method}`,
//     params,
//   });
//   if (!result) {
//     notify({
//       title: 'Error',
//       text: 'Error calling contract method',
//       type: 'error',
//     });
//   }
// };

const responseMessage = ref('');

const getContractState = async () =>
  // contractAddress: string,
  // method: string,
  // methodArguments: any[],
  {
    responseMessage.value = '';

    try {
      const result = await contractsStore.getContractState(
        contractsStore.deployedContract?.address || '',
        props.methodName,
        Object.values(inputs.value),
      );

      responseMessage.value = JSON.stringify(result);
      console.log(result);
    } catch (error) {
      notify({
        title: 'Error',
        text: (error as Error)?.message || 'Error getting contract state',
        type: 'error',
      });
    }
  };

const callMethod = async () => {
  const result = await contractsStore.callContractMethod({
    userAccount: accountsStore.currentUserAddress || '',
    localContractId: contractsStore.deployedContract?.contractId || '',
    method: `${props.methodName}`,
    params: Object.values(inputs.value),
  });

  // console.log({ result });

  clearInputs();

  // const params = Object.values(inputs.value[selectedMethod.value.name] || {});
  // emit('callMethod', { method: selectedMethod.value.name, params });
  // inputs.value[selectedMethod.value.name] = {};
};

const clearInputs = () => {
  inputs.value = {};
};
</script>

<template>
  <div
    class="dark:bg-g flex flex-col overflow-hidden rounded-md bg-slate-100 dark:bg-gray-700"
  >
    <button
      class="flex grow flex-row items-center justify-between p-2 text-xs hover:bg-slate-200 dark:hover:bg-gray-600"
      @click="isExpanded = !isExpanded"
    >
      {{ methodName }}

      <ChevronDownIcon
        class="h-4 w-4 opacity-70 transition-all duration-300"
        :class="isExpanded && 'rotate-180'"
      />
    </button>

    <Collapse :when="isExpanded">
      <div class="flex flex-col items-start p-2">
        <component
          v-for="(inputType, inputKey) in method.inputs"
          :key="inputKey"
          :is="InputTypesMap[inputType]"
          v-model="inputs[inputKey]"
          :name="String(inputKey)"
          :label="String(inputKey)"
          :placeholder="String(inputKey)"
        />

        <Btn v-if="methodType === 'read'" @click="getContractState" tiny
          >Read</Btn
        >

        <Btn v-if="methodType === 'write'" @click="callMethod" tiny>Write</Btn>

        <div v-if="responseMessage" class="break-all text-sm">
          Response:
          <div class="rounded bg-white p-1 dark:bg-slate-600">
            {{ responseMessage }}
          </div>
        </div>
      </div>
    </Collapse>
  </div>
</template>
