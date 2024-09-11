<script setup lang="ts">
import type { ContractMethod } from '@/types';
import { onMounted, ref, computed } from 'vue';
import { Collapse } from 'vue-collapsed';
import { useInputMap } from '@/hooks';
import { notify } from '@kyvg/vue3-notification';
import { ChevronDownIcon } from '@heroicons/vue/16/solid';
import { useEventTracking, useContractQueries } from '@/hooks';

const { callWriteMethod, callReadMethod, contract } = useContractQueries();
const { trackEvent } = useEventTracking();

const inputMap = useInputMap();

const props = defineProps<{
  method: ContractMethod;
  methodType: 'read' | 'write';
}>();

const isExpanded = ref(false);
const inputs = ref<{ [k: string]: any }>({});
const responseMessage = ref('');

const missingParams = computed(() => {
  return props.method.inputs.some(
    (input: any) => inputs.value[input.name] === '',
  );
});

const handleCallReadMethod = async () => {
  responseMessage.value = '';

  try {
    const result = await callReadMethod(
      props.method.name,
      Object.values(inputs.value),
    );

    responseMessage.value = JSON.stringify(result);

    trackEvent('called_read_method', {
      contract_name: contract.value?.name || '',
      method_name: props.method.name,
    });
  } catch (error) {
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error getting contract state',
      type: 'error',
    });
  }
};

const handleCallWriteMethod = async () => {
  await callWriteMethod({
    method: props.method.name,
    params: Object.values(inputs.value),
  });

  resetInputs();

  notify({
    text: 'Write method called',
    type: 'success',
  });

  trackEvent('called_write_method', {
    contract_name: contract.value?.name || '',
    method_name: props.method.name,
  });
};

const resetInputs = () => {
  props.method.inputs.forEach((input: any) => {
    let defaultValue;

    switch (input.type) {
      case 'uint256':
      case 'float':
        defaultValue = 0;
        break;
      case 'bool':
        defaultValue = false;
        break;
      case 'string':
        defaultValue = '';
        break;
      default:
        defaultValue = '';
        break;
    }

    inputs.value[input.name] = defaultValue;
  });
};

onMounted(() => {
  resetInputs();
});
</script>

<template>
  <div
    class="dark:bg-g flex flex-col overflow-hidden rounded-md bg-slate-100 dark:bg-gray-700"
  >
    <button
      class="flex grow flex-row items-center justify-between bg-slate-200 p-2 text-xs hover:bg-slate-300 dark:bg-slate-600 dark:hover:bg-slate-500"
      @click="isExpanded = !isExpanded"
      :data-testid="`expand-method-btn-${method.name}`"
    >
      <div class="truncate">
        {{ method.name }}
      </div>

      <ChevronDownIcon
        class="h-4 w-4 opacity-70 transition-all duration-300"
        :class="isExpanded && 'rotate-180'"
      />
    </button>

    <Collapse :when="isExpanded">
      <div class="flex flex-col items-start gap-2 p-2">
        <component
          v-for="input in method.inputs"
          :key="input.name"
          :is="inputMap.getComponent(input.type)"
          v-model="inputs[input.name]"
          :name="String(input.name)"
          :label="String(input.name)"
          :placeholder="String(input.name)"
        />

        <div>
          <Btn
            v-if="methodType === 'read'"
            @click="handleCallReadMethod"
            tiny
            :data-testid="`read-method-btn-${method.name}`"
            :disabled="missingParams"
            v-tooltip="missingParams ? 'All parameters are required' : ''"
            >Call Contract</Btn
          >

          <Btn
            v-if="methodType === 'write'"
            @click="handleCallWriteMethod"
            tiny
            :data-testid="`write-method-btn-${method.name}`"
            >Send Transaction</Btn
          >
        </div>

        <div v-if="responseMessage" class="w-full break-all text-sm">
          <div class="mb-1 text-xs font-medium">Response:</div>
          <div
            :data-testid="`method-response-${method.name}`"
            class="w-full rounded bg-white p-1 font-mono text-xs dark:bg-slate-600"
          >
            {{ responseMessage }}
          </div>
        </div>
      </div>
    </Collapse>
  </div>
</template>
