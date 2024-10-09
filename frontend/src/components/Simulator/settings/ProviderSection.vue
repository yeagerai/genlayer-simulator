<script setup lang="ts">
import { useNodeStore, useContractsStore } from '@/stores';
import { ref, computed } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { PlusIcon } from '@heroicons/vue/16/solid';
import { uniqBy } from 'lodash-es';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ProviderItem from '@/components/Simulator/ProviderItem.vue';
import ProviderModal from '@/components/Simulator/ProviderModal.vue';
import { DatabaseBackup } from 'lucide-vue-next';
import { notify } from '@kyvg/vue3-notification';

const nodeStore = useNodeStore();
const isNewProviderModalOpen = ref(false);
const isResetProvidersModalOpen = ref(false);
const isResetting = ref(false);

const modelGroups = computed(() => {
  return uniqBy(nodeStore.nodeProviders, 'provider').map((provider: any) => ({
    provider: provider.provider,
    models: nodeStore.nodeProviders.filter(
      (p) => p.provider === provider.provider,
    ),
  }));
});

const handleResetProviders = async () => {
  isResetting.value = true;

  try {
    await nodeStore.resetProviders();

    notify({
      title: 'Successfully reset providers',
      type: 'success',
    });
  } catch (error) {
    console.error(error);
    notify({
      title: 'Could not reset providers',
      type: 'error',
    });
  } finally {
    isResetting.value = false;
    isResetProvidersModalOpen.value = false;
  }
};
</script>

<template>
  <PageSection>
    <template #title>Provider Configs</template>

    <template #actions>
      <GhostBtn
        @click="isNewProviderModalOpen = true"
        v-tooltip="'New Config'"
        testId="create-new-validator-btn"
      >
        <PlusIcon class="h-4 w-4" />
      </GhostBtn>
    </template>

    <div v-for="group in modelGroups" :key="group.provider">
      <div class="mb-1 text-xs font-semibold opacity-50">
        {{ group.provider }}
      </div>
      <!-- {{ group.models.some((model) => !model.is_available) }} -->

      <div
        class="overflow-hidden rounded-md border border-gray-300 dark:border-gray-800"
        v-if="nodeStore.validators.length > 0"
      >
        <div class="divide-y divide-gray-200 dark:divide-gray-800"></div>
        <ProviderItem
          v-for="model in group.models"
          :key="model.id"
          :provider="model"
        />
      </div>
    </div>

    <ProviderModal
      :open="isNewProviderModalOpen"
      @close="isNewProviderModalOpen = false"
    />

    <Btn
      v-if="nodeStore.nodeProviders.length > 0"
      @click="isResetProvidersModalOpen = true"
      :icon="DatabaseBackup"
      secondary
    >
      Reset Providers
    </Btn>

    <ConfirmationModal
      :open="isResetProvidersModalOpen"
      @confirm="handleResetProviders"
      @close="isResetProvidersModalOpen = false"
      buttonText="Reset Providers"
      buttonTestId="btn-reset-providers"
      :dangerous="true"
      :confirming="isResetting"
    >
      <template #title>Reset Provider Configs</template>
      <template #description
        >Are you sure? All providers and models will be reset to the default
        values.</template
      >
    </ConfirmationModal>
  </PageSection>
</template>
