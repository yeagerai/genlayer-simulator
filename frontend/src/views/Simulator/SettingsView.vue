<script setup lang="ts">
import { onMounted } from 'vue';
import { notify } from '@kyvg/vue3-notification';
import { useNodeStore } from '@/stores';
import ValidatorItem from '@/components/Simulator/ValidatorItem.vue';
import ValidatorModal from '@/components/Simulator/ValidatorModal.vue';
import { ref } from 'vue';
import MainTitle from '@/components/Simulator/MainTitle.vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArchiveBoxXMarkIcon } from '@heroicons/vue/24/solid';
import { PlusIcon } from '@heroicons/vue/16/solid';
const nodeStore = useNodeStore();
const isNewValidatorModalOpen = ref(false);

// Hooks
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
const handleResetStorage = async () => {
  try {
    await nodeStore.resetStorage();
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
    nodeStore.closeResetStorageModal();
  }
};
</script>

<template>
  <div class="flex max-h-[93vh] w-full flex-col overflow-y-auto">
    <MainTitle data-testid="settings-page-title">Settings</MainTitle>

    <PageSection id="tutorial-validators">
      <template #title>
        Validators <span class="opacity-50">{{ nodeStore.validators.length }}</span>
      </template>

      <div class="flex flex-col gap-2">
        <ValidatorItem
          v-for="validator in nodeStore.validators"
          :key="validator.id"
          :validator="validator"
        />
      </div>

      <Btn @click="isNewValidatorModalOpen = true" data-testid="create-new-validator-btn">
        <PlusIcon class="h-5 w-5" />
        New Validator
      </Btn>

      <ValidatorModal :open="isNewValidatorModalOpen" @close="isNewValidatorModalOpen = false" />
    </PageSection>

    <PageSection>
      <template #title>Simulator Storage</template>

      <Btn
        @click="nodeStore.openResetStorageModal"
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
      :open="nodeStore.resetStorageModalOpen"
      @confirm="handleResetStorage"
      @close="nodeStore.closeResetStorageModal"
      buttonText="Reset Storage"
      buttonTestId="btn-reset-storage"
      :dangerous="true"
      :confirming="nodeStore.resettingStorage"
    >
      <template #title>Reset Simulator Storage</template>
      <template #description
        >Are you sure? All the examples will be restored, and the following intelligent contracts
        will be removed.</template
      >

      <template #info>
        <div class="text-xs" v-for="contract in nodeStore.contractsToDelete" :key="contract.id">
          {{ contract.name }}
        </div>
      </template>

      <div class="mt-1 text-xs italic">
        <span class="font-semibold">Note:</span> if you want to preserve any of these contracts,
        make a copy of them in the files section.
      </div>
    </ConfirmationModal>
  </div>
</template>
