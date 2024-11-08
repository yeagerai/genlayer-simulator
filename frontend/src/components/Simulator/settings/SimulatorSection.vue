<script setup lang="ts">
import { notify } from '@kyvg/vue3-notification';
import { useNodeStore, useContractsStore } from '@/stores';
import { ref } from 'vue';
import PageSection from '@/components/Simulator/PageSection.vue';
import { ArchiveXIcon } from 'lucide-vue-next';

const contractsStore = useContractsStore();
const nodeStore = useNodeStore();
const isResetStorageModalOpen = ref(false);
const isResetting = ref(false);

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
  <PageSection>
    <template #title>Storage</template>

    <Btn
      @click="isResetStorageModalOpen = true"
      :icon="ArchiveXIcon"
      :disabled="nodeStore.contractsToDelete.length < 1"
      secondary
      v-tooltip="
        nodeStore.contractsToDelete.length < 1 && 'No contracts files to delete'
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
      <template #title>Reset Studio Storage</template>
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
  </PageSection>
</template>
