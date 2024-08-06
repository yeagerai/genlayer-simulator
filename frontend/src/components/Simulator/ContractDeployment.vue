<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import { ref, computed, watch, onMounted } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import { InputTypesMap } from '@/utils';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import { Collapse } from 'vue-collapsed';
import GhostBtn from '../global/GhostBtn.vue';
import { notify } from '@kyvg/vue3-notification';
import TextAreaInput from '@/components/global/inputs/TextAreaInput.vue';
import FieldError from '@/components/global/fields/FieldError.vue';

const {
  schema,
  contractSchemaQuery,
  deployContract,
  contractAbiQuery,
  // constructorInputs,
  isDeployed,
  isDeploying,
  address,
} = useContractQueries();

const { data, error, isPending, isRefetching, isError } = contractSchemaQuery;
const inputParams = ref<{ [k: string]: any }>({});

const constructorInputs = computed<{ [k: string]: string }>(
  () => data.value?.methods['__init__']?.inputs,
);

watch(
  () => constructorInputs.value,
  (newVal) => {
    console.log(watch);
    inputParams.value = {
      ...inputParams.value,
      ...constructorInputs.value,
    };
  },
);

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
    // TODO: fix this logic
    const l1 = Object.keys(constructorInputs.value).length;
    const l2 = Object.keys(inputParams.value).length;
    console.log(l1, l2);
    return l1 === l2;
  }
});
const jsonParams = ref('{}');

const mode = ref<'json' | 'form'>('form');

// TODO:
const handleDeployContract = () => {
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

  deployContract({ constructorParams });
};

const setInputParams = (inputs: { [k: string]: string }) => {
  inputParams.value = Object.keys(inputs)
    .map((key) => ({ name: key, value: inputs[key] }))
    .reduce((prev, curr) => {
      switch (curr.value) {
        case 'bool':
          prev = { ...prev, [curr.name]: false };
          break;
        case 'str':
          prev = { ...prev, [curr.name]: '' };
          break;
        case 'int':
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
    .map((key) => ({ name: key, type: InputTypesMap[key], value: inputs[key] }))
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
    setInputParams(newValue || {});
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
    <template #title>Deploy</template>

    <template #actions>
      <Loader v-if="isRefetching" />
    </template>

    <div
      v-if="isPending"
      class="flex flex-row items-center justify-center gap-2 p-1"
    >
      <Loader />
      Loading...
    </div>

    <Alert v-else-if="isError" error>
      {{ error?.message }}
    </Alert>

    <template v-else-if="data">
      <!-- <pre>
        {{ constructorInputs }}
      </pre>
      <pre>
        {{ inputParams }}
      </pre> -->
      <!-- {{ isValidDefaultState }} -->
      <!-- {{ inputParams }} -->
      <div class="flex flex-row items-center justify-between gap-1">
        Constructor inputs

        <GhostBtn
          v-if="hasConstructorInputs"
          @click="toggleMode"
          class="p-1 text-xs"
        >
          {{ mode === 'json' ? 'Inputs' : 'JSON' }}
        </GhostBtn>
      </div>

      <EmptyListPlaceholder v-if="!hasConstructorInputs">
        No constructor inputs.
      </EmptyListPlaceholder>

      <div v-else class="flex flex-col justify-start">
        <div
          v-if="mode === 'form'"
          v-for="(inputType, input) in constructorInputs"
          :key="input"
        >
          <!-- <FieldLabel :for="`${input}`">{{ input }}</FieldLabel> -->

          <!-- <label :for="`${input}`" class="mr-2 text-xs">{{ input }}</label> -->
          <!-- TODO: dedicated field components -->
          <component
            :is="InputTypesMap[inputType]"
            v-model="inputParams[input]"
            :name="input"
            :placeholder="input"
            :label="input"
          />
        </div>

        <TextAreaInput
          v-if="mode === 'json'"
          name="State"
          :rows="5"
          :invalid="!isValidDefaultState"
          class="w-full bg-slate-100 p-2 dark:dark:bg-zinc-700"
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
      >
        <template v-if="isDeploying"> Deploying... </template>
        <template v-else-if="isDeployed">
          <ArrowUpTrayIcon class="h-4 w-4" />
          Re-deploy
        </template>
        <template v-else>
          <ArrowUpTrayIcon class="h-4 w-4" />
          Deploy
        </template>
      </Btn>
      <ToolTip v-if="!isValidDefaultState" text="Provide default state" />
    </template>
  </PageSection>
</template>
