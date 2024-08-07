<script setup lang="ts">
import { useContractQueries } from '@/hooks/useContractQueries';
import PageSection from '@/components/Simulator/PageSection.vue';
import { CheckCircleIcon } from '@heroicons/vue/24/outline';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import { PlusIcon } from '@heroicons/vue/16/solid';
import { shortenAddress } from '@/utils';

defineProps<{
  showNewDeploymentButton: boolean;
}>();

const emit = defineEmits(['openDeployment']);
const { isDeployed, address, contract } = useContractQueries();
</script>

<template>
  <PageSection>
    <template #title
      >Contract
      <div data-testid="current-contract-name" class="opacity-50">
        {{ contract?.name }}
      </div></template
    >

    <div
      v-if="isDeployed"
      data-testid="deployed-contract-info"
      class="flex flex-row items-center gap-1 text-xs"
    >
      <CheckCircleIcon class="h-4 w-4 shrink-0 text-emerald-400" />

      Deployed at

      <div class="font-semibold">
        {{ shortenAddress(address) }}
      </div>

      <CopyTextButton :text="address" />
    </div>

    <EmptyListPlaceholder v-else>Not deployed yet.</EmptyListPlaceholder>

    <Btn
      secondary
      tiny
      class="inline-flex w-auto shrink grow-0"
      v-if="showNewDeploymentButton"
      @click="emit('openDeployment')"
    >
      <PlusIcon class="h-4 w-4 shrink-0" />
      New Deployment
    </Btn>
  </PageSection>
</template>
