<script setup lang="ts">
import { useContractQueries, useInputMap } from '@/hooks';
import { ref, computed, watch, onMounted } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import GhostBtn from '../global/GhostBtn.vue';
import { notify } from '@kyvg/vue3-notification';
import TextAreaInput from '@/components/global/inputs/TextAreaInput.vue';
import FieldError from '@/components/global/fields/FieldError.vue';
import { type ContractMethod } from '@/types';
import * as calldata from '@/calldata';

const props = defineProps<{
  leaderOnly: boolean;
}>();

const { contract, contractSchemaQuery, deployContract, isDeploying } =
  useContractQueries();
const inputMap = useInputMap();

const { data, isPending, isRefetching, isError } = contractSchemaQuery;
const inputParams = ref<{ [k: string]: any }>({});

const constructorInputs = computed(
  () =>
    (data.value?.abi as ContractMethod[] | undefined)?.find(
      (method) => method.type === 'constructor',
    )?.inputs,
);

const emit = defineEmits(['deployed-contract']);

const isValidDefaultState = computed(() => {
  if (mode.value === 'json') {
    // Try to parse JSON
    try {
      JSON.parse(jsonParams.value || '{}');
      return true;
    } catch (error) {
      return false;
    }
  } else {
    return true;
  }
});

const jsonParams = ref('{}');
const mode = ref<'json' | 'form'>('form');

const handleDeployContract = async () => {
  let constructorParams: calldata.CalldataEncodable[];

  if (mode.value === 'json') {
    try {
      const data = calldata.parse(jsonParams.value || '{}');
      if (!(data instanceof Array)) {
        throw new Error('constructor parameters must be an array');
      }
      constructorParams = data;
    } catch (error) {
      console.error(error);
      notify({
        title: 'Error',
        text: 'Please provide valid JSON',
        type: 'error',
      });
      return;
    }
  } else {
    constructorParams = Object.keys(inputParams.value).map((key) => {
      const val = inputParams.value[key];
      if (
        constructorInputs.value?.find((x) => x.name === key)?.type === 'string'
      ) {
        return val;
      }
      return calldata.parse(val);
    });
  }

  await deployContract(constructorParams, props.leaderOnly);

  emit('deployed-contract');
};

const setInputParams = (inputs: { [k: string]: any }) => {
  inputParams.value = inputs
    .map((input: any) => ({ name: input.name, type: input.type }))
    .reduce((prev: any, curr: any) => {
      switch (curr.type) {
        case 'bool':
          prev = { ...prev, [curr.name]: 'false' };
          break;
        case 'string':
          prev = { ...prev, [curr.name]: '' };
          break;
        case 'int':
          prev = { ...prev, [curr.name]: '0' };
          break;
        case 'None':
          prev = { ...prev, [curr.name]: 'null' };
          break;
        default:
          prev = { ...prev, [curr.name]: '' };
          break;
      }
      return prev;
    }, {});

  jsonParams.value = JSON.stringify(inputParams.value || {}, null, 2);
};

const toggleMode = () => {
  mode.value = mode.value === 'json' ? 'form' : 'json';
  if (mode.value === 'json') {
    throw new Error('json is unsupported right now');
  } else {
    inputParams.value = {};
  }
};

watch(
  () => constructorInputs.value,
  (newValue) => {
    setInputParams(newValue || []);
  },
);

onMounted(() => {
  if (constructorInputs.value) {
    setInputParams(constructorInputs.value);
  }
});

const hasConstructorInputs = computed(
  () =>
    constructorInputs.value && Object.keys(constructorInputs.value).length > 0,
);
</script>

<template>
  <PageSection>
    <template #title
      >Constructor Inputs
      <Loader v-if="isRefetching" :size="14" />
    </template>

    <template #actions>
      <GhostBtn
        v-if="hasConstructorInputs"
        @click="toggleMode"
        class="p-1 text-xs"
      >
        {{ mode === 'json' ? 'Inputs' : 'JSON' }}
      </GhostBtn>
    </template>

    <ContentLoader v-if="isPending" />

    <Alert v-else-if="isError" error> Could not load contract schema. </Alert>

    <template v-else-if="data">
      <EmptyListPlaceholder v-if="!hasConstructorInputs">
        No constructor inputs.
      </EmptyListPlaceholder>

      <div
        v-else
        class="flex flex-col justify-start gap-1"
        :class="isDeploying && 'pointer-events-none opacity-60'"
      >
        <template v-if="mode === 'form'">
          <div v-for="input in constructorInputs" :key="input.name">
            <component
              :is="inputMap.getComponent(input.type)"
              v-model="inputParams[input.name]"
              :name="input.name"
              :placeholder="input.name"
              :label="input.name"
            />
          </div>
        </template>

        <TextAreaInput
          v-if="mode === 'json'"
          id="state"
          name="state"
          :rows="5"
          :invalid="!isValidDefaultState"
          v-model="jsonParams"
        />
        <FieldError v-if="!isValidDefaultState"
          >Please enter valid JSON.</FieldError
        >
      </div>

      <Btn
        testId="btn-deploy-contract"
        @click="handleDeployContract"
        :loading="isDeploying"
        :disabled="!isValidDefaultState"
        :icon="ArrowUpTrayIcon"
        v-tooltip="!isValidDefaultState && 'Provide default state'"
      >
        <template v-if="isDeploying">Deploying...</template>
        <template v-else>Deploy {{ contract?.name }}</template>
      </Btn>
    </template>
  </PageSection>
</template>
