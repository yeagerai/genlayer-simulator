<script setup lang="ts">
import { useContractQueries, useInputMap } from '@/hooks';
import { ref, computed, watch, onMounted } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
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

const handleDeployContract = async () => {
  let constructorParams = Object.keys(inputParams.value).map((key) => {
    const val = inputParams.value[key];

    if (typeof val === 'string') {
      return val;
    }

    return calldata.parse(String(val));
  });

  await deployContract(constructorParams, props.leaderOnly);

  emit('deployed-contract');
};

const setInputParams = (inputs: { [k: string]: any }) => {
  inputParams.value = inputs
    .map((input: any) => ({
      name: input.name,
      type: input.type,
      default: input.default,
    }))
    .reduce((prev: any, curr: any) => {
      switch (curr.type) {
        case 'bool':
          prev = { ...prev, [curr.name]: false };
          break;
        case 'string':
          prev = { ...prev, [curr.name]: curr.default || '' };
          break;
        case 'int':
          prev = { ...prev, [curr.name]: 0 };
          break;
        default:
          prev = { ...prev, [curr.name]: curr.default || '' };
          break;
      }
      return prev;
    }, {});
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
        <div v-for="input in constructorInputs" :key="input.name">
          <component
            :is="inputMap.getComponent(input.type)"
            v-model="inputParams[input.name]"
            :name="input.name"
            :placeholder="input.name"
            :label="input.name"
          />
        </div>
      </div>

      <Btn
        testId="btn-deploy-contract"
        @click="handleDeployContract"
        :loading="isDeploying"
        :icon="ArrowUpTrayIcon"
      >
        <template v-if="isDeploying">Deploying...</template>
        <template v-else>Deploy {{ contract?.name }}</template>
      </Btn>
    </template>
  </PageSection>
</template>
