<script setup lang="ts">
import { useNodeStore, useContractsStore } from '@/stores';
import { ref, computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { PlusIcon } from '@heroicons/vue/16/solid';
import { uniqBy } from 'lodash-es';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ProviderItem from '@/components/Simulator/ProviderItem.vue';
import ProviderModal from '@/components/Simulator/ProviderModal.vue';

const nodeStore = useNodeStore();
const isNewProviderModalOpen = ref(false);

const modelGroups = computed(() => {
  return uniqBy(nodeStore.nodeProviders, 'provider').map((provider: any) => ({
    provider: provider.provider,
    models: nodeStore.nodeProviders.filter(
      (p) => p.provider === provider.provider,
    ),
  }));
});
</script>

<template>
  <PageSection>
    <template #title>Providers</template>

    <template #actions>
      <GhostBtn
        @click="isNewProviderModalOpen = true"
        v-tooltip="'New Provider'"
        testId="create-new-validator-btn"
      >
        <PlusIcon class="h-4 w-4" />
      </GhostBtn>
    </template>

    <div v-for="group in modelGroups" :key="group.provider">
      {{ group.provider }} :

      <div
        class="overflow-hidden rounded-md border border-gray-300 dark:border-gray-800"
        v-if="nodeStore.validators.length > 0"
      >
        <div class="divide-y divide-gray-200 dark:divide-gray-800"></div>
        <ProviderItem
          v-for="model in group.models"
          :key="model"
          :provider="model"
        />
      </div>
    </div>

    <ProviderModal
      :open="true || isNewProviderModalOpen"
      @close="isNewProviderModalOpen = false"
    />
  </PageSection>
</template>
