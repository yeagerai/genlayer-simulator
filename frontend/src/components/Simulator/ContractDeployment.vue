<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import { ref, computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import { InputTypesMap } from '@/utils';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';

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

const isValidDefaultState = computed(() => {
  const l1 = Object.keys(constructorInputs.value).length;
  const l2 = Object.keys(inputParams.value).length;
  console.log(l1, l2);
  return l1 === l2;
});
</script>

<template>
  <PageSection>
    <template #title>Deploy</template>

    <template #actions>
      <Loader v-if="isRefetching" />
    </template>

    <span v-if="isPending">Loading...</span>

    <Alert v-else-if="isError" error>
      {{ error?.message }}
    </Alert>

    <template v-else-if="data">
      {{ constructorInputs }}
      <!-- {{ inputParams }} -->

      <div class="flex flex-row items-center gap-1">Constructor inputs</div>

      <EmptyListPlaceholder
        v-if="constructorInputs && Object.keys(constructorInputs).length === 0"
      >
        No constructor inputs.
      </EmptyListPlaceholder>

      <div
        v-else
        class="flex items-center justify-between py-2"
        v-for="(inputType, input) in constructorInputs"
        :key="input"
      >
        <label :for="`${input}`" class="mr-2 text-xs">{{ input }}</label>
        <input
          v-model="inputParams[input]"
          :name="`${input}`"
          :type="InputTypesMap[inputType]"
          :placeholder="`${input}`"
          class="bg-slate-100 p-2 dark:dark:bg-zinc-700"
          label="Input"
        />
      </div>

      <Btn
        testId="btn-deploy-contract"
        @click="deployContract({ constructorParams: inputParams })"
        :loading="isDeploying"
      >
        <ArrowUpTrayIcon class="h-4 w-4" />
        {{ isDeploying ? 'Deploying...' : isDeployed ? 'Re-deploy' : 'Deploy' }}
      </Btn>
      <ToolTip v-if="!isValidDefaultState" text="Provide default state" />
    </template>
  </PageSection>
</template>
