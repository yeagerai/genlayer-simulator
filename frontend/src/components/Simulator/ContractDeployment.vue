<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import { ref, computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArrowUpTrayIcon } from '@heroicons/vue/16/solid';
import { InputTypesMap } from '@/utils';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import LoadingIndicator from '@/components/LoadingIndicator.vue';

// FIXME: stopped while playing around with background fetching state when changing contract code
// FIXME: breaks some stuff around constructorInputs ( any way to not do ' v-if="constructorInputs && Object.keys(constructorInputs).length === 0" ' ? )

const {
  schema,
  contractSchemaQuery,
  deployContract,
  contractAbiQuery,
  constructorInputs,
  isDeployed,
  isDeploying,
  address,
} = useContractQueries();

const { data, isLoading, isFetching, error } = contractSchemaQuery;
const inputParams = ref<{ [k: string]: any }>({});
</script>

<template>
  <PageSection>
    <template #title>Deploy</template>
    <!-- <div v-if="isLoading">Loading...</div>
    <div v-else-if="error">
      {{ error }}
    </div>
    <div v-else> -->
    <div class="flex flex-row items-center gap-1">
      Constructor inputs
      <LoadingIndicator :size="12" v-if="isFetching" />
    </div>

    <EmptyListPlaceholder
      v-if="constructorInputs && Object.keys(constructorInputs).length === 0"
    >
      No constructor inputs.
    </EmptyListPlaceholder>

    <!-- <pre class="text-xs">{{ constructorInputs }}</pre> -->
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
    <!-- </div> -->

    <Btn
      testId="btn-deploy-contract"
      @click="deployContract({ constructorParams: inputParams })"
      :loading="isDeploying"
    >
      <ArrowUpTrayIcon class="h-4 w-4" />
      {{ isDeploying ? 'Deploying...' : isDeployed ? 'Re-deploy' : 'Deploy' }}
    </Btn>
  </PageSection>
</template>
