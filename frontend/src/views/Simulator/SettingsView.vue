<script setup lang="ts">
import { onMounted } from 'vue';
import { notify } from '@kyvg/vue3-notification';
import { useNodeStore, useContractsStore } from '@/stores';
import ValidatorItem from '@/components/Simulator/ValidatorItem.vue';
import ValidatorModal from '@/components/Simulator/ValidatorModal.vue';
import { ref } from 'vue';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArchiveBoxXMarkIcon } from '@heroicons/vue/24/solid';
import { PlusIcon } from '@heroicons/vue/16/solid';

const contractsStore = useContractsStore();
const nodeStore = useNodeStore();
const isNewValidatorModalOpen = ref(false);

onMounted(async () => {
  try {
    await nodeStore.getValidatorsData();
  } catch (error) {
    console.error(error);
    notify({
      title: 'Error',
      text: (error as Error)?.message || 'Error loading validators',
      type: 'error',
    });
  }
});

// TODO: refac
const isResetStorageModalOpen = ref(false);
const isResetting = ref(false);

const handleResetStorage = async () => {
  isResetting.value = true;
  try {
    await contractsStore.resetStorage();

    notify({
      title: 'Success',
      text: 'Storage reset successfully',
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

      <div
        class="overflow-hidden rounded-md border border-gray-300 dark:border-gray-800"
        v-if="nodeStore.validators.length > 0"
      >
        <div class="divide-y divide-gray-200 dark:divide-gray-800">
          <ValidatorItem
            v-for="validator in nodeStore.validators"
            :key="validator.id"
            :validator="validator"
          />
        </div>
      </div>

      <Btn
        @click="isNewValidatorModalOpen = true"
        data-testid="create-new-validator-btn"
      >
        <PlusIcon class="h-5 w-5" />
        New Validator
      </Btn>

      <ValidatorModal
        :open="isNewValidatorModalOpen"
        @close="isNewValidatorModalOpen = false"
      />
    </PageSection>

    <PageSection>
      <template #title>Simulator Storage</template>

      <Btn
        @click="isResetStorageModalOpen = true"
        :disabled="nodeStore.contractsToDelete.length < 1"
        secondary
      >
        <ArchiveBoxXMarkIcon class="h-4 w-4" />
        Reset Storage
      </Btn>

      <ToolTip
        text="No Contracts file to delete"
        :options="{ placement: 'right' }"
        v-if="nodeStore.contractsToDelete.length < 1"
      />
    </PageSection>

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
        <span class="font-semibold">Note:</span> if you want to preserve any of
        these contracts, make a copy of them in the files section.
      </div>
    </ConfirmationModal>
  </div>
</template>
