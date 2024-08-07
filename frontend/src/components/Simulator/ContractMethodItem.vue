<script setup lang="ts">
import type { ContractMethod } from '@/types';
import { ref } from 'vue';
import { Collapse } from 'vue-collapsed';
import { InputTypesMap } from '@/utils';
import { useAccountsStore } from '@/stores';
import { useContractQueries } from '@/hooks/useContractQueries';
import { notify } from '@kyvg/vue3-notification';
import { ChevronDownIcon } from '@heroicons/vue/16/solid';

const { callWriteMethod, callReadMethod } = useContractQueries();
const accountsStore = useAccountsStore();

const props = defineProps<{
  methodName: string;
  method: ContractMethod;
  methodType: 'read' | 'write';
}>();

const isExpanded = ref(false);
const inputs = ref<{ [k: string]: any }>({});
const responseMessage = ref('');

const handleCallReadMethod = async () => {
  responseMessage.value = '';

  try {
    const result = await callReadMethod(
      props.methodName,
      Object.values(inputs.value),
    );

    console.log(result);

    responseMessage.value = JSON.stringify(result);
  } catch (error) {
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error getting contract state',
      type: 'error',
    });
  }
};

const handleCallWriteMethod = async () => {
  const result = await callWriteMethod({
    userAccount: accountsStore.currentUserAddress || '',
    method: props.methodName,
    params: Object.values(inputs.value),
  });

  console.log(result);
  clearInputs();
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
      class="flex grow flex-row items-center justify-between bg-slate-200 p-2 text-xs hover:bg-slate-300 dark:bg-slate-600 dark:hover:bg-slate-500"
      @click="isExpanded = !isExpanded"
      :data-testid="`expand-method-btn-${methodName}`"
      >
      <div class="truncate">
        {{ methodName }}
      </div>

      <ChevronDownIcon
        class="h-4 w-4 opacity-70 transition-all duration-300"
        :class="isExpanded && 'rotate-180'"
      />
    </button>

    <Collapse :when="isExpanded">
      <div class="flex flex-col items-start gap-2 p-2">
        <component
          v-for="(inputType, inputKey) in method.inputs"
          :key="inputKey"
          :is="InputTypesMap[inputType]"
          v-model="inputs[inputKey]"
          :name="String(inputKey)"
          :label="String(inputKey)"
          :placeholder="String(inputKey)"
        />

        <div>
          <Btn
            v-if="methodType === 'read'"
            @click="handleCallReadMethod"
            tiny
            :data-testid="`read-method-btn-${methodName}`"
            >Read</Btn
          >

          <Btn
            v-if="methodType === 'write'"
            @click="handleCallWriteMethod"
            tiny
            :data-testid="`write-method-btn-${methodName}`"
            >Write</Btn
          >
        </div>

        <div v-if="responseMessage" class="w-full break-all text-sm">
          <div class="mb-1 text-xs font-medium">Response:</div>
          <div
            :data-testid="`method-response-${methodName}`"
            class="w-full rounded bg-white p-1 font-mono text-xs dark:bg-slate-600"
          >
            {{ responseMessage }}
          </div>
        </div>
      </div>
    </Collapse>
  </div>
</template>
