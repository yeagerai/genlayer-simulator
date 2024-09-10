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

const { contract, contractSchemaQuery, deployContract, isDeploying } =
  useContractQueries();
const inputMap = useInputMap();

const { data, isPending, isRefetching, isError } = contractSchemaQuery;
const inputParams = ref<{ [k: string]: any }>({});

const constructorInputs = computed(
  () =>
    data.value?.abi.find(
      (method: ContractMethod) => method.type === 'constructor',
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
  let constructorParams = {};

  if (mode.value === 'json') {
    try {
      const json = JSON.parse(jsonParams.value || '{}');
      constructorParams = mapInputs(json);
    } catch (error) {
      console.error(error);
      notify({
        title: 'Error',
        text: 'Please provide valid JSON',
        type: 'error',
      });
    }
  } else {
    constructorParams = mapInputs(inputParams.value);
  }

  await deployContract({ constructorParams });

  emit('deployed-contract');
};

const setInputParams = (inputs: { [k: string]: any }) => {
  inputParams.value = inputs
    .map((input: any) => ({ name: input.name, type: input.type }))
    .reduce((prev: any, curr: any) => {
      switch (curr.type) {
        case 'bool':
          prev = { ...prev, [curr.name]: false };
          break;
        case 'string':
          prev = { ...prev, [curr.name]: '' };
          break;
        case 'uint256':
          prev = { ...prev, [curr.name]: 0 };
          break;
        case 'float':
          prev = { ...prev, [curr.name]: 0.0 };
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
    jsonParams.value = JSON.stringify(inputParams.value || {}, null, 2);
  } else {
    inputParams.value = JSON.parse(jsonParams.value || '{}');
  }
};

const mapInputs = (inputs: { [k: string]: string }) =>
  Object.keys(inputs || {})
    .map((key) => ({
      name: key,
      type: inputs[key],
      value: inputs[key],
    }))
    .reduce((prev, curr) => {
      if (typeof curr.value === 'boolean') {
        prev = { ...prev, [curr.name]: curr.value ? 'True' : 'False' };
      } else {
        prev = { ...prev, [curr.name]: curr.value };
      }

      return prev;
    }, {});

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
          <div v-for="input in constructorInputs" :key="input">
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
