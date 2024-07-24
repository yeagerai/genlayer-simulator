<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { InputTypesMap } from '@/utils';
import { useAccountsStore } from '@/stores';
import type { ContractMethod } from '@/types';
import LoadingIndicator from '@/components/LoadingIndicator.vue';
interface Abi {
  methods: {
    [k: string]: {
      inputs: { [k: string]: string };
    };
  };
  class: string;
}

interface Props {
  abi?: Abi;
  callingMethod: boolean;
}

const store = useAccountsStore();
const props = defineProps<Props>();
const emit = defineEmits(['callMethod']);
const methodList = ref<ContractMethod[]>([]);
const method = ref<ContractMethod>();

const inputs = computed<{ [k: string]: any }>(() => {
  return methodList.value.reduce((prev: any, curr) => {
    prev[curr.name] = {};
    return prev;
  }, {});
});

watch(
  () => props.abi,
  (newValue) => {
    method.value = undefined;
    methodList.value = Object.entries(newValue?.methods || {})
      .filter((m) => !m[0].startsWith('_') && !m[0].startsWith('get_'))
      .map((m) => ({
        name: m[0],
        inputs: m[1].inputs,
      }));
  }
);

const handleMethodCall = () => {
  if (method.value) {
    const params = Object.values(inputs.value[method.value.name] || {});
    emit('callMethod', { method: method.value.name, params });
    inputs.value[method.value.name] = {};
  }
};

const onMethodChange = (event: Event) => {
  const selectedMethod = (event.target as HTMLSelectElement).value;
  if (selectedMethod) {
    method.value = methodList.value.find((m) => m.name === selectedMethod);
  } else method.value = undefined;
};

const setCurentUserAddress = (event: Event) => {
  if ((event.target as HTMLSelectElement)?.value) {
    store.currentPrivateKey = (event.target as HTMLSelectElement)
      ?.value as `0x${string}`;
  }
};
</script>

<template>
  <div
    class="mt-6 flex w-full flex-col bg-slate-100 px-2 py-2 dark:bg-zinc-700"
  >
    <h5 class="text-sm">Execute Transactions</h5>
  </div>
  <div class="flex flex-col overflow-y-auto p-2">
    <div class="flex w-full flex-col items-start">
      <p>Current Account:</p>
      <select
        name="dropdown-current-account"
        @change="setCurentUserAddress"
        class="w-full text-xs dark:bg-zinc-700"
        :value="store.currentUserAddress"
      >
        <option :value="store.currentUserAddress">
          {{ store.currentUserAddress }}
        </option>
        <option
          v-for="privateKey in store.privateKeys"
          :key="privateKey"
          :value="privateKey"
        >
          {{ store.accountFromPrivateKey(privateKey).address }}
        </option>
      </select>
    </div>
    <div class="mt-4 flex w-full justify-start">
      <select
        name="dropdown-execute-method"
        @change="onMethodChange"
        class="w-full dark:bg-zinc-700"
      >
        <option value="">Select a method</option>
        <option
          v-for="method in methodList"
          :key="method.name"
          :value="method.name"
        >
          {{ method.name }}()
        </option>
      </select>
    </div>
    <template v-if="method">
      <div class="mt-4 flex w-full flex-col">
        <div
          class="flex items-center justify-between py-2"
          v-for="(inputType, input) in method.inputs"
          :key="input"
        >
          <label :for="`${input}`" class="mr-2 text-xs">{{ input }}</label>
          <input
            v-model="inputs[method.name][input]"
            :name="`${input}`"
            :type="InputTypesMap[inputType]"
            :placeholder="`${input}`"
            class="bg-slate-100 p-2 dark:dark:bg-zinc-700"
            label="Input"
          />
        </div>
      </div>
      <div class="mt-4 flex w-full flex-col">
        <ToolTip
          :text="`Execute ${method.name}()`"
          :options="{ placement: 'top' }"
        />
        <button
          @click="handleMethodCall"
          class="rounded bg-primary px-4 py-2 font-semibold text-white hover:opacity-80"
        >
          <LoadingIndicator v-if="props.callingMethod" :color="'white'" />
          <template v-else>Execute{{ ` ${method.name}` }}()</template>
        </button>
      </div>
    </template>
    <div id="tutorial-creating-transactions" class="flex"></div>
  </div>
</template>

<style>
.editor {
  width: 100% !important;
  min-height: 20rem !important;
}
</style>
