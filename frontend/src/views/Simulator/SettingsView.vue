<script setup lang="ts">
import { notify } from '@kyvg/vue3-notification';
import { useNodeStore, useContractsStore } from '@/stores';
import ValidatorItem from '@/components/Simulator/ValidatorItem.vue';
import ValidatorModal from '@/components/Simulator/ValidatorModal.vue';
import { ref, computed } from 'vue';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArchiveBoxXMarkIcon } from '@heroicons/vue/24/solid';
import { PlusIcon } from '@heroicons/vue/16/solid';
import EmptyListPlaceholder from '@/components/Simulator/EmptyListPlaceholder.vue';
import { uniqBy } from 'lodash-es';
import GhostBtn from '@/components/global/GhostBtn.vue';
import ProviderItem from '@/components/Simulator/ProviderItem.vue';
import ProviderModal from '@/components/Simulator/ProviderModal.vue';

const contractsStore = useContractsStore();
const nodeStore = useNodeStore();
const isNewValidatorModalOpen = ref(false);
const isNewProviderModalOpen = ref(false);
const isResetStorageModalOpen = ref(false);
const isResetting = ref(false);

const modelGroups = computed(() => {
  return uniqBy(nodeStore.nodeProviders, 'provider').map((provider: any) => ({
    provider: provider.provider,
    models: nodeStore.nodeProviders.filter(
      (p) => p.provider === provider.provider,
    ),
  }));
});

const handleResetStorage = async () => {
  isResetting.value = true;
  try {
    await contractsStore.resetStorage();

    notify({
      title: 'Storage reset successfully',
      type: 'success',
    });
  } catch (error) {
    console.error(error);
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error resetting the storage',
      type: 'error',
    });
  } finally {
    isResetStorageModalOpen.value = false;
    isResetting.value = false;
  }
};
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <MainTitle data-testid="settings-page-title">Settings</MainTitle>

    <PageSection id="tutorial-validators">
      <template #title>
        Validators
        <span class="opacity-50">{{ nodeStore.validators.length }}</span>
      </template>

      <template #actions>
        <GhostBtn
          @click="isNewValidatorModalOpen = true"
          v-tooltip="'New Validator'"
          testId="create-new-validator-btn"
        >
          <PlusIcon class="h-4 w-4" />
        </GhostBtn>
      </template>

      <ContentLoader v-if="nodeStore.isLoadingValidatorData" />

      <EmptyListPlaceholder v-else-if="nodeStore.validators.length < 1">
        No validators.
      </EmptyListPlaceholder>

      <div
        class="overflow-hidden rounded-md border border-gray-300 dark:border-gray-800"
        v-if="nodeStore.validators.length > 0"
      >
        <div class="divide-y divide-gray-200 dark:divide-gray-800">
          <ValidatorItem
            v-for="validator in nodeStore.validatorsOrderedById"
            :key="validator.id"
            :validator="validator"
          />
        </div>
      </div>

      <Btn
        v-if="
          !nodeStore.hasAtLeastOneValidator && !nodeStore.isLoadingValidatorData
        "
        @click="isNewValidatorModalOpen = true"
        :icon="PlusIcon"
      >
        New Validator
      </Btn>

      <ValidatorModal
        :open="isNewValidatorModalOpen"
        @close="isNewValidatorModalOpen = false"
      />
    </PageSection>

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
        :open="isNewProviderModalOpen"
        @close="isNewProviderModalOpen = false"
      />

      <!-- <GhostBtn
        @click="
          nodeStore.addProvider({
            provider: 'openai',
            model: 'gpt-4o-mini',
            config: {},
            plugin: 'openai',
            plugin_config: {
              api_key_env_var: 'OPENAIKEY',
              api_url: null,
            },
          })
        "
        >Add Provider</GhostBtn
      > -->
    </PageSection>

    <PageSection>
      <template #title>Simulator Storage</template>

      <Btn
        @click="isResetStorageModalOpen = true"
        :icon="ArchiveBoxXMarkIcon"
        :disabled="nodeStore.contractsToDelete.length < 1"
        secondary
        v-tooltip="
          nodeStore.contractsToDelete.length < 1 &&
          'No contracts files to delete'
        "
      >
        Reset Storage
      </Btn>

      <ConfirmationModal
        :open="isResetStorageModalOpen"
        @confirm="handleResetStorage"
        @close="isResetStorageModalOpen = false"
        buttonText="Reset Storage"
        buttonTestId="btn-reset-storage"
        :dangerous="true"
        :confirming="isResetting"
      >
        <template #title>Reset Simulator Storage</template>
        <template #description
          >Are you sure? All the examples will be restored, and the following
          intelligent contracts will be removed.</template
        >

        <template #info>
          <div
            class="text-xs"
            v-for="contract in nodeStore.contractsToDelete"
            :key="contract.id"
          >
            {{ contract.name }}
          </div>
        </template>

        <div class="mt-1 text-xs italic">
          <span class="font-semibold">Note:</span> if you want to preserve any
          of these contracts, make a copy of them in the files section.
        </div>
      </ConfirmationModal>
    </PageSection>
  </div>
</template>
